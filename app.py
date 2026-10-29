
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import torch

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
)
from sklearn.neural_network import MLPClassifier
from pytorch_tabnet.tab_model import TabNetClassifier
from imblearn.over_sampling import SMOTE

st.set_page_config(page_title="ASD Detection", page_icon="🧠", layout="wide")
st.title("Interpretable Deep Learning for Early ASD Detection")
st.write("Compare TabNet and MLP models using your dataset.")
st.warning(
    "This is a research demonstration, not a diagnostic tool. "
    "Predictions must not replace professional clinical assessment."
)

uploaded_file = st.file_uploader(
    "Upload your ASD dataset (CSV or Excel)",
    type=["csv", "xls", "xlsx"]
)

if uploaded_file is not None:
            try:
            uploaded_file.seek(0)

            if uploaded_file.name.lower().endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            else:
                try:
                    data = pd.read_excel(uploaded_file)
                except Exception:
                    uploaded_file.seek(0)
                    data = pd.read_csv(uploaded_file)

        except Exception as e:
            st.error(f"Could not read the uploaded dataset: {e}")
            st.stop()



        st.subheader("Dataset preview")
        st.write("Dataset shape:", data.shape)
        st.dataframe(data.head())

        if "Case_No" in data.columns:
            data = data.drop(columns=["Case_No"])

        data = data.ffill()

        data = data.rename(columns={
            "A1": "Q1", "A2": "Q2", "A3": "Q3",
            "A4": "Q4", "A5": "Q5", "A6": "Q6",
            "A7": "Q7", "A8": "Q8", "A9": "Q9",
            "A10": "Q10", "Age_Mons": "Age",
            "Family_mem_with_ASD": "Family_ASD",
            "Who_completed_the_test": "Screener",
            "Class/ASD Traits ": "ASD"
        })

        if "ASD" not in data.columns:
            st.error(
                "Target column not found. Check that your dataset "
                "contains 'Class/ASD Traits ' or 'ASD'."
            )
            st.stop()

        questions = [f"Q{i}" for i in range(1, 11)]
        missing = [c for c in questions if c not in data.columns]

        if missing:
            st.error(f"Missing questionnaire columns: {missing}")
            st.stop()

        data = data.dropna(subset=["ASD"]).copy()

        # Remove rows with missing values in other columns
        data = data.dropna().copy()

        if data.empty:
            st.error("No usable rows remain after preprocessing.")
            st.stop()

        # Encode categorical columns consistently
        encoders = {}
        for col in data.select_dtypes(include=["object", "category"]).columns:
            encoder = LabelEncoder()
            data[col] = encoder.fit_transform(data[col].astype(str))
            encoders[col] = encoder

        data[questions] = data[questions].apply(
            pd.to_numeric, errors="coerce"
        )

        if "Age" in data.columns:
            data["Age"] = pd.to_numeric(data["Age"], errors="coerce")

        data = data.dropna().copy()

        data["AQ10"] = data[questions].sum(axis=1)
        data["A_domain"] = data[questions[:9]].sum(axis=1)
        data["B_domain"] = data["Q10"]

        X = data.drop(columns=["ASD"])
        y = data["ASD"].astype(int)

        if y.nunique() != 2:
            st.error("This app expects a binary ASD target with two classes.")
            st.stop()

        # Split before fitting the scaler or resampling
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Scale Age using training data only
        if "Age" in X.columns:
            scaler = StandardScaler()
            X_train = X_train.copy()
            X_test = X_test.copy()
            X_train.loc[:, "Age"] = scaler.fit_transform(
                X_train[["Age"]]
            ).ravel()
            X_test.loc[:, "Age"] = scaler.transform(
                X_test[["Age"]]
            ).ravel()

        # SMOTE must only be applied to training data
        counts = y_train.value_counts()
        if len(counts) < 2 or counts.min() < 2:
            st.error("Not enough minority-class training samples for SMOTE.")
            st.stop()

        smote = SMOTE(random_state=42, k_neighbors=min(5, int(counts.min()) - 1))
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

        st.subheader("Training models")
        with st.spinner("Training TabNet and MLP. This may take several minutes..."):
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
                X_train_res.to_numpy(dtype=np.float32),
                y_train_res.to_numpy(),
                eval_set=[
                    (
                        X_test.to_numpy(dtype=np.float32),
                        y_test.to_numpy()
                    )
                ],
                max_epochs=100,
                patience=10,
                batch_size=256,
                virtual_batch_size=128
            )

            mlp = MLPClassifier(
                hidden_layer_sizes=(16, 8),
                max_iter=200,
                alpha=0.1,
                early_stopping=True,
                validation_fraction=0.2,
                random_state=42
            )
            mlp.fit(X_train_res, y_train_res)

        tabnet_pred = tabnet.predict(
            X_test.to_numpy(dtype=np.float32)
        ).ravel().astype(int)

        mlp_prob = mlp.predict_proba(X_test)[:, 1]
        mlp_pred = (mlp_prob >= 0.6).astype(int)

        st.success("Model training completed.")

        def show_metrics(name, actual, predicted):
            st.subheader(name)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Accuracy", f"{accuracy_score(actual, predicted):.3f}")
            c2.metric("Precision", f"{precision_score(actual, predicted, zero_division=0):.3f}")
            c3.metric("Recall", f"{recall_score(actual, predicted, zero_division=0):.3f}")
            c4.metric("F1 Score", f"{f1_score(actual, predicted, zero_division=0):.3f}")

            st.text("Classification report")
            st.text(classification_report(actual, predicted, zero_division=0))

            fig, ax = plt.subplots()
            sns.heatmap(
                confusion_matrix(actual, predicted),
                annot=True, fmt="d", cmap="Blues", ax=ax
            )
            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")
            st.pyplot(fig)
            plt.close(fig)

        show_metrics("TabNet Results", y_test, tabnet_pred)
        show_metrics("MLP Results", y_test, mlp_pred)

        st.subheader("MLP ROC Curve")
        fpr, tpr, _ = roc_curve(y_test, mlp_prob)
        roc_auc = auc(fpr, tpr)

        fig, ax = plt.subplots()
        ax.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
        ax.plot([0, 1], [0, 1], linestyle="--")
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("TabNet Feature Importance")
        importance = pd.Series(
            tabnet.feature_importances_, index=X.columns
        ).sort_values()

        st.bar_chart(importance)

        st.subheader("MLP Training Information")
        st.write("Training iterations:", mlp.n_iter_)

       except Exception as e:
        st.error(f"Unable to process the dataset: {e}")
        st.info(
            "Check the dataset columns and file format. "
            "If the error persists, share the full error message."
        )

else:
    st.info("Upload your dataset to train and evaluate the models.")
