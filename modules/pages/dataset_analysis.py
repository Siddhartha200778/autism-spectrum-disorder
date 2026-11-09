import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from modules.theme import render_section_header, apply_chart_theme, render_disclaimer
from modules.ml_pipeline import load_dataset_from_bytes, load_default_dataset, preprocess_and_prepare, train_models_pipeline

def render():
    render_section_header(
        "Clinical Dataset Explorer & Ingestion",
        "Upload and inspect pediatric autism screening callsets, explore demographic distributions, and run preprocessing.",
        badge="DATA MANAGEMENT & PREPROCESSING"
    )

    # Ingestion Controls
    st.subheader("1. Dataset Ingestion")
    up_col1, up_col2 = st.columns([2.5, 1.5])
    
    with up_col1:
        uploaded_file = st.file_uploader(
            "Drag and drop your ASD dataset (CSV, XLS, XLSX)",
            type=["csv", "xls", "xlsx"],
            help="Supports standard toddler screening formats containing Q1-Q10 or A1-A10 questions and ASD class labels."
        )

    with up_col2:
        st.write("**Or use the built-in research dataset:**")
        if st.button("📁 Load Benchmark Dataset", use_container_width=True, help="Loads toddler_asd_dataset.csv (1,054 toddler records)"):
            with st.spinner("Loading benchmark dataset..."):
                raw_df = load_default_dataset()
                if raw_df is not None:
                    st.session_state["raw_dataset"] = raw_df
                    st.session_state["dataset_source"] = "Toddler ASD Screening Dataset (toddler_asd_dataset.csv)"
                    st.session_state["dataset_size"] = f"{raw_df.shape[0]:,} records &bull; 71.2 KB"
                    # Reset models to trigger retraining
                    st.session_state["data_preprocessed"] = False
                    st.success("Loaded Toddler ASD dataset successfully!")
                    st.rerun()

    # Process uploaded file if provided
    if uploaded_file is not None:
        try:
            raw_bytes = uploaded_file.getvalue()
            size_kb = len(raw_bytes) / 1024
            raw_df = load_dataset_from_bytes(raw_bytes, uploaded_file.name)
            
            st.session_state["raw_dataset"] = raw_df
            st.session_state["dataset_source"] = uploaded_file.name
            st.session_state["dataset_size"] = f"{size_kb:.1f} KB"
            st.session_state["data_preprocessed"] = False
            st.success(f"Successfully uploaded and parsed **{uploaded_file.name}** ({size_kb:.1f} KB)!")
        except Exception as e:
            st.error(f"Error parsing uploaded file: {e}")
            return

    if "raw_dataset" not in st.session_state or st.session_state["raw_dataset"] is None:
        st.info("Please upload a dataset or click 'Load Benchmark Dataset' above to inspect data.")
        return

    raw_df = st.session_state["raw_dataset"]
    source_name = st.session_state.get("dataset_source", "Custom Dataset")
    file_size = st.session_state.get("dataset_size", "N/A")

    # Dataset Metadata Stats
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("2. Dataset Overview & Dimensions")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active File", source_name)
    m2.metric("File Size", file_size)
    m3.metric("Total Records (Rows)", f"{raw_df.shape[0]:,}")
    m4.metric("Total Features (Cols)", f"{raw_df.shape[1]}")

    # Dataset Preview
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("3. Data Sample Preview")
    st.dataframe(raw_df.head(10), use_container_width=True)

    # Missing Value & Column Diagnostics
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("4. Data Quality & Missing Value Diagnostics")
    
    col_missing, col_types = st.columns(2)
    with col_missing:
        null_counts = raw_df.isnull().sum()
        total_missing = null_counts.sum()
        if total_missing == 0:
            st.success("**Zero Missing Values Detected.** All records are fully populated.")
        else:
            st.warning(f"**{total_missing} missing values detected across {sum(null_counts > 0)} columns.** Preprocessing will apply forward-fill and row filtering.")
            df_missing = pd.DataFrame({
                "Column": null_counts.index,
                "Missing Values": null_counts.values,
                "Percentage (%)": (null_counts.values / len(raw_df) * 100).round(2)
            })
            st.dataframe(df_missing[df_missing["Missing Values"] > 0], use_container_width=True)

    with col_types:
        st.write("**Column Data Types & Non-Null Counts:**")
        df_info = pd.DataFrame({
            "Column Name": raw_df.columns,
            "Detected Type": [str(t) for t in raw_df.dtypes],
            "Non-Null Count": raw_df.notnull().sum().values
        })
        st.dataframe(df_info, use_container_width=True, height=250)

    # Visual Distributions
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("5. Demographic & Clinical Distributions")

    c_g1, c_g2 = st.columns(2)
    with c_g1:
        # Check target column
        target_col = None
        for cand in ["Class/ASD Traits ", "Class/ASD Traits", "ASD"]:
            if cand in raw_df.columns:
                target_col = cand
                break
        
        if target_col:
            fig, ax = plt.subplots(figsize=(6, 3.8))
            val_counts = raw_df[target_col].astype(str).value_counts()
            colors = ["#167C80", "#14243A"]
            ax.bar(val_counts.index, val_counts.values, color=colors[:len(val_counts)], width=0.55, edgecolor="#202B36", linewidth=1.2)
            ax.set_title("Target Class Distribution (ASD Traits)", fontsize=11, fontweight="bold", color="#202B36", pad=12)
            ax.set_ylabel("Count", fontweight="bold")
            apply_chart_theme(fig, ax)
            st.pyplot(fig)
            plt.close(fig)

    with c_g2:
        # Check Age or Age_Mons column
        age_col = None
        for cand in ["Age_Mons", "Age"]:
            if cand in raw_df.columns:
                age_col = cand
                break
        
        if age_col:
            fig, ax = plt.subplots(figsize=(6, 3.8))
            ages = pd.to_numeric(raw_df[age_col], errors="coerce").dropna()
            ax.hist(ages, bins=15, color="#167C80", edgecolor="#14243A", alpha=0.85)
            ax.set_title(f"Toddler Age Distribution ({age_col})", fontsize=11, fontweight="bold", color="#202B36", pad=12)
            ax.set_xlabel("Age (Months)", fontweight="bold")
            ax.set_ylabel("Frequency", fontweight="bold")
            apply_chart_theme(fig, ax)
            st.pyplot(fig)
            plt.close(fig)

    # Train / Retrain Action
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("6. Preprocess & Train AI Models")
    st.write("Run the full preprocessing pipeline (Case_No dropping, label encoding, standard scaling, SMOTE resampling) and train TabNet and MLP neural networks.")

    if st.button("Preprocess Dataset & Train Models", type="primary", use_container_width=True):
        with st.spinner("Executing preprocessing, SMOTE balance resampler, and training TabNet and MLP models..."):
            try:
                prep = preprocess_and_prepare(raw_df)
                models = train_models_pipeline(prep)
                st.session_state["prepared_data"] = prep
                st.session_state["models_result"] = models
                st.session_state["data_preprocessed"] = True
                st.success("✅ Models successfully trained on the dataset! Navigate to 'AI Models', 'Model Comparison', or 'Results & Visualization' to explore findings.")
            except Exception as e:
                st.error(f"Preprocessing / Training Error: {e}")

    render_disclaimer()
