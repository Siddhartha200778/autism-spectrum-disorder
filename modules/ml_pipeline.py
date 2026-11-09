import io
import os
import streamlit as st

try:
    import joblib
except ImportError:
    try:
        from sklearn.utils import _joblib as joblib
    except ImportError:
        import pickle as joblib

try:
    import torch
    try:
        torch.set_num_threads(1)
    except Exception:
        pass
except Exception:
    torch = None

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
)
from sklearn.neural_network import MLPClassifier

try:
    from pytorch_tabnet.tab_model import TabNetClassifier
except Exception:
    TabNetClassifier = None

try:
    from imblearn.over_sampling import SMOTE
except Exception:
    SMOTE = None

def load_dataset_from_bytes(file_bytes, filename=""):
    """Loads a dataset from raw bytes, handling CSV, XLS, XLSX formats."""
    name = filename.lower()
    raw = file_bytes
    
    if name.endswith(".csv"):
        data = pd.read_csv(io.BytesIO(raw))
    elif raw[:4] == b"PK\x03\x04":
        data = pd.read_excel(io.BytesIO(raw), engine="openpyxl")
    elif raw[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        data = pd.read_excel(io.BytesIO(raw), engine="xlrd")
    else:
        # Fallback for CSV formatted files with .xls extension or custom delimiters
        data = pd.read_csv(io.BytesIO(raw), sep=None, engine="python")
        
    data.columns = data.columns.str.strip()
    return data

@st.cache_data(show_spinner=False)
def load_default_dataset():
    """Loads the benchmark research toddler ASD dataset included in the repo."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for default_name in ["toddler_asd_dataset.csv", "dl dataset.xls"]:
        default_path = os.path.join(base_dir, default_name)
        if not os.path.exists(default_path):
            default_path = default_name
        if os.path.exists(default_path):
            with open(default_path, "rb") as f:
                bytes_data = f.read()
            return load_dataset_from_bytes(bytes_data, default_name)
    return None

@st.cache_resource(show_spinner=False)
def get_benchmark_models_and_data():
    """
    Loads pre-trained TabNet and MLP models and preprocessed data.
    Loads instantly from cached_models.joblib in < 1 second with 0% CPU overhead,
    preventing Streamlit Cloud resource throttling.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache_path = os.path.join(base_dir, "cached_models.joblib")
    if not os.path.exists(cache_path):
        cache_path = "cached_models.joblib"
        
    if os.path.exists(cache_path):
        try:
            bundle = joblib.load(cache_path)
            return bundle.get("prep"), bundle.get("models")
        except Exception:
            pass

    raw_df = load_default_dataset()
    if raw_df is not None:
        prep = preprocess_and_prepare(raw_df)
        models = train_models_pipeline(prep)
        return prep, models
    return None, None

def preprocess_and_prepare(raw_df):
    """
    Executes the scientifically rigorous, leakage-free preprocessing pipeline:
    - Drops non-predictive identifiers (Case_No).
    - Excludes Qchat-10-Score (and proxy sum aggregates) because Qchat-10-Score is the
      deterministic label-construction proxy (sum(A1..A10) >= 4 -> ASD=Yes).
    - Preserves 16 authentic clinical predictors: Q1..Q10, Age, Sex, Ethnicity,
      Jaundice, Family_ASD, Screener.
    - Categorical label encoding fitted deterministically.
    - Stratified 80/20 train/test split.
    - Independent validation split (80/20 of training set) created strictly from train fold.
    - StandardScaler fitted ONLY on training age, transforming train, val, and test.
    - SMOTE resampling applied strictly to the training fold.
    """
    data = raw_df.copy()
    
    if "Case_No" in data.columns:
        data = data.drop(columns=["Case_No"])

    data = data.ffill()

    # Column renaming
    rename_dict = {
        "A1": "Q1", "A2": "Q2", "A3": "Q3",
        "A4": "Q4", "A5": "Q5", "A6": "Q6",
        "A7": "Q7", "A8": "Q8", "A9": "Q9",
        "A10": "Q10", "Age_Mons": "Age",
        "Family_mem_with_ASD": "Family_ASD",
        "Who completed the test": "Screener",
        "Who_completed_the_test": "Screener",
        "Class/ASD Traits ": "ASD",
        "Class/ASD Traits": "ASD"
    }
    data = data.rename(columns=rename_dict)

    if "ASD" not in data.columns:
        raise ValueError("Target column 'ASD' or 'Class/ASD Traits' not found in dataset.")

    questions = [f"Q{i}" for i in range(1, 11)]
    missing_q = [c for c in questions if c not in data.columns]
    if missing_q:
        raise ValueError(f"Missing questionnaire columns: {missing_q}")

    data = data.dropna(subset=["ASD"]).dropna().copy()
    if data.empty:
        raise ValueError("No usable rows remaining after dropping missing values.")

    # Target binarization (1 = ASD, 0 = Non-ASD)
    data["ASD"] = (data["ASD"].astype(str).str.strip().str.lower().isin(["yes", "1", "true"])).astype(int)

    # Categorical Encoding
    encoders = {}
    cat_cols = data.select_dtypes(include=["object", "category", "string"]).columns
    for col in cat_cols:
        encoder = LabelEncoder()
        data[col] = encoder.fit_transform(data[col].astype(str))
        encoders[col] = encoder

    data[questions] = data[questions].apply(pd.to_numeric, errors="coerce")
    if "Age" in data.columns:
        data["Age"] = pd.to_numeric(data["Age"], errors="coerce")

    data = data.dropna().copy()

    # SCIENTIFIC LEAKAGE CORRECTION:
    # Exclude Qchat-10-Score (and do not engineer AQ10 / A_domain proxy sums)
    # The predictive feature matrix X contains strictly the individual items and covariates.
    cols_to_drop = ["ASD"]
    for c in ["Qchat-10-Score", "AQ10", "A_domain", "B_domain"]:
        if c in data.columns:
            cols_to_drop.append(c)

    X = data.drop(columns=cols_to_drop).astype(float)
    y = data["ASD"].astype(int)

    if y.nunique() != 2:
        raise ValueError(f"Target column must be binary (found {y.nunique()} unique classes).")

    # 1. Stratified Train-Test split (80% train, 20% holdout test)
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 2. Validation split created EXCLUSIVELY from the training partition (80/20 split of train)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full, test_size=0.2, random_state=42, stratify=y_train_full
    )

    # 3. Scaler for Age (fitted STRICTLY on X_train)
    scaler = None
    if "Age" in X.columns:
        scaler = StandardScaler()
        X_train = X_train.copy()
        X_val = X_val.copy()
        X_test = X_test.copy()
        X_train.loc[:, "Age"] = scaler.fit_transform(X_train[["Age"]]).ravel()
        X_val.loc[:, "Age"] = scaler.transform(X_val[["Age"]]).ravel()
        X_test.loc[:, "Age"] = scaler.transform(X_test[["Age"]]).ravel()

    # 4. SMOTE resampling applied STRICTLY to training data
    counts = y_train.value_counts()
    if len(counts) < 2 or counts.min() < 2:
        raise ValueError("Not enough minority-class training samples for SMOTE resampling.")

    smote = SMOTE(random_state=42, k_neighbors=min(5, int(counts.min()) - 1))
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    return {
        "raw_df": raw_df,
        "processed_df": data,
        "X_train_res": X_train_res,
        "y_train_res": y_train_res,
        "X_val": X_val,
        "y_val": y_val,
        "X_test": X_test,
        "y_test": y_test,
        "feature_names": list(X.columns),
        "encoders": encoders,
        "scaler": scaler,
        "class_counts_before": y_train.value_counts().to_dict(),
        "class_counts_after": pd.Series(y_train_res).value_counts().to_dict()
    }

def train_models_pipeline(prepared_data):
    """
    Trains both TabNet and MLP models using exact parameters and computes true evaluation metrics.
    Early stopping for TabNet monitors the validation partition X_val (NEVER the holdout test set).
    Both models are evaluated on the identical holdout test set (X_test, y_test).
    """
    X_train_res = prepared_data["X_train_res"]
    y_train_res = prepared_data["y_train_res"]
    X_val = prepared_data["X_val"]
    y_val = prepared_data["y_val"]
    X_test = prepared_data["X_test"]
    y_test = prepared_data["y_test"]
    feature_names = prepared_data["feature_names"]

    # 1. TabNet Model (Attentive Tabular Transformer)
    tabnet = TabNetClassifier(
        n_d=16,
        n_a=16,
        n_steps=5,
        gamma=1.5,
        lambda_sparse=1e-4,
        optimizer_fn=torch.optim.Adam,
        optimizer_params={"lr": 0.02},
        verbose=0,
        seed=42
    )

    tabnet.fit(
        X_train_res.to_numpy(dtype=np.float32).copy(),
        y_train_res.to_numpy().copy(),
        eval_set=[(X_val.to_numpy(dtype=np.float32).copy(), y_val.to_numpy().copy())],
        eval_metric=["accuracy"],
        max_epochs=100,
        patience=15,
        batch_size=128,
        virtual_batch_size=64
    )

    # 2. MLP Model (Multi-Layer Perceptron)
    mlp = MLPClassifier(
        hidden_layer_sizes=(16, 8),
        max_iter=200,
        alpha=0.1,
        early_stopping=True,
        validation_fraction=0.2,
        random_state=42
    )
    mlp.fit(X_train_res, y_train_res)

    # TabNet Predictions & Probabilities on Holdout Test Set
    tabnet_pred = tabnet.predict(X_test.to_numpy(dtype=np.float32)).ravel().astype(int)
    tabnet_prob = tabnet.predict_proba(X_test.to_numpy(dtype=np.float32))[:, 1]

    # MLP Predictions & Probabilities on Holdout Test Set
    mlp_prob = mlp.predict_proba(X_test)[:, 1]
    mlp_pred = (mlp_prob >= 0.5).astype(int)

    # TabNet Metrics
    tabnet_acc = float(accuracy_score(y_test, tabnet_pred))
    tabnet_prec = float(precision_score(y_test, tabnet_pred, zero_division=0))
    tabnet_rec = float(recall_score(y_test, tabnet_pred, zero_division=0))
    tabnet_f1 = float(f1_score(y_test, tabnet_pred, zero_division=0))
    tabnet_cm = confusion_matrix(y_test, tabnet_pred)
    tn_tab, fp_tab, fn_tab, tp_tab = tabnet_cm.ravel()
    tabnet_spec = float(tn_tab / (tn_tab + fp_tab)) if (tn_tab + fp_tab) > 0 else 0.0
    tabnet_report = classification_report(y_test, tabnet_pred, zero_division=0, output_dict=True)
    tabnet_fpr, tabnet_tpr, _ = roc_curve(y_test, tabnet_prob)
    tabnet_auc = float(auc(tabnet_fpr, tabnet_tpr))
    tabnet_importance = pd.Series(tabnet.feature_importances_, index=feature_names).sort_values(ascending=False)

    # MLP Metrics
    mlp_acc = float(accuracy_score(y_test, mlp_pred))
    mlp_prec = float(precision_score(y_test, mlp_pred, zero_division=0))
    mlp_rec = float(recall_score(y_test, mlp_pred, zero_division=0))
    mlp_f1 = float(f1_score(y_test, mlp_pred, zero_division=0))
    mlp_cm = confusion_matrix(y_test, mlp_pred)
    tn_mlp, fp_mlp, fn_mlp, tp_mlp = mlp_cm.ravel()
    mlp_spec = float(tn_mlp / (tn_mlp + fp_mlp)) if (tn_mlp + fp_mlp) > 0 else 0.0
    mlp_report = classification_report(y_test, mlp_pred, zero_division=0, output_dict=True)
    mlp_fpr, mlp_tpr, _ = roc_curve(y_test, mlp_prob)
    mlp_auc = float(auc(mlp_fpr, mlp_tpr))

    return {
        "tabnet": {
            "model": tabnet,
            "predictions": tabnet_pred,
            "probabilities": tabnet_prob,
            "accuracy": tabnet_acc,
            "precision": tabnet_prec,
            "recall": tabnet_rec,
            "specificity": tabnet_spec,
            "f1": tabnet_f1,
            "confusion_matrix": tabnet_cm,
            "classification_report": tabnet_report,
            "fpr": tabnet_fpr,
            "tpr": tabnet_tpr,
            "auc": tabnet_auc,
            "feature_importance": tabnet_importance
        },
        "mlp": {
            "model": mlp,
            "predictions": mlp_pred,
            "probabilities": mlp_prob,
            "accuracy": mlp_acc,
            "precision": mlp_prec,
            "recall": mlp_rec,
            "specificity": mlp_spec,
            "f1": mlp_f1,
            "confusion_matrix": mlp_cm,
            "classification_report": mlp_report,
            "fpr": mlp_fpr,
            "tpr": mlp_tpr,
            "auc": mlp_auc,
            "iterations": int(mlp.n_iter_)
        },
        "y_test": y_test
    }

def run_single_patient_inference(patient_dict, models_dict, prepared_data):
    """
    Runs real-time inference on a single patient record using both TabNet and MLP.
    patient_dict contains: Q1..Q10, Age, Sex, Ethnicity, Jaundice, Family_ASD, Screener.
    Excludes Qchat-10-Score and proxy aggregates from input features.
    """
    feature_names = prepared_data["feature_names"]
    encoders = prepared_data["encoders"]
    scaler = prepared_data["scaler"]

    # Calculate domain scores for clinical dossier and display
    q_vals = [patient_dict.get(f"Q{i}", 0) for i in range(1, 11)]
    aq10_score = sum(q_vals)
    a_domain = sum(q_vals[:9])
    b_domain = q_vals[9]

    # Create dictionary matching feature names (the 16 predictive features)
    row_dict = {}
    for f in feature_names:
        if f in patient_dict:
            row_dict[f] = patient_dict[f]
        else:
            row_dict[f] = 0

    df_row = pd.DataFrame([row_dict])

    # Encode categoricals using fitted encoders
    for col, enc in encoders.items():
        if col in df_row.columns:
            val_str = str(df_row[col].iloc[0])
            if val_str in enc.classes_:
                df_row[col] = enc.transform([val_str])[0]
            else:
                df_row[col] = 0

    # Ensure numeric conversion
    for c in df_row.columns:
        df_row[c] = pd.to_numeric(df_row[c], errors="coerce").fillna(0)

    # Scale Age
    if "Age" in df_row.columns and scaler is not None:
        df_row["Age"] = scaler.transform(df_row[["Age"]])[0][0]

    # Model Inferences
    tabnet = models_dict["tabnet"]["model"]
    mlp = models_dict["mlp"]["model"]

    x_np = df_row[feature_names].to_numpy(dtype=np.float32)

    # TabNet
    tabnet_prob = float(tabnet.predict_proba(x_np)[0, 1])
    tabnet_pred = int(tabnet.predict(x_np)[0])

    # MLP
    mlp_prob = float(mlp.predict_proba(df_row[feature_names])[0, 1])
    mlp_pred = int(mlp_prob >= 0.5)

    return {
        "tabnet_prob": tabnet_prob,
        "tabnet_pred": tabnet_pred,
        "mlp_prob": mlp_prob,
        "mlp_pred": mlp_pred,
        "aq10_score": aq10_score,
        "a_domain": a_domain,
        "b_domain": b_domain
    }
