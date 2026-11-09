import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from modules.theme import render_section_header, apply_chart_theme, render_disclaimer

def render():
    render_section_header(
        "Clinical Analytics & Visualization Dashboard",
        "Comprehensive visualization suite showcasing actual dataset statistics, dual confusion matrices, ROC analysis, and feature salience.",
        badge="CLINICAL ANALYTICS"
    )

    if "models_result" not in st.session_state or "prepared_data" not in st.session_state:
        st.info("💡 The models are initializing on the benchmark dataset...")
        return

    models = st.session_state["models_result"]
    prepared = st.session_state["prepared_data"]
    tabnet = models["tabnet"]
    mlp = models["mlp"]

    # 1. Dataset & Resampling Statistics
    st.subheader("1. Cohort & Resampling Balance Statistics")
    
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Preprocessed Records", f"{len(prepared['processed_df']):,}")
    s2.metric("Evaluated Test Records", f"{len(prepared['y_test']):,}")
    s3.metric("Pre-SMOTE (Non-ASD : ASD)", f"{prepared['class_counts_before'].get(0, 0)} : {prepared['class_counts_before'].get(1, 0)}")
    s4.metric("Post-SMOTE Balanced Folds", f"{prepared['class_counts_after'].get(0, 0)} : {prepared['class_counts_after'].get(1, 0)}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Side-by-Side Confusion Matrices
    st.subheader("2. Dual Confusion Matrices (Hold-Out Test Cohort)")
    cm_col1, cm_col2 = st.columns(2)

    with cm_col1:
        st.write("**TabNet Confusion Matrix:**")
        fig, ax = plt.subplots(figsize=(5.5, 4.2))
        sns.heatmap(
            tabnet["confusion_matrix"], annot=True, fmt="d", cmap=sns.light_palette("#167C80", as_cmap=True), cbar=False, ax=ax,
            annot_kws={"size": 13, "weight": "bold"}
        )
        ax.set_xlabel("Predicted Class", fontweight="bold", fontsize=10)
        ax.set_ylabel("Actual Class", fontweight="bold", fontsize=10)
        ax.set_xticklabels(["Non-ASD (0)", "ASD (1)"], fontweight="bold")
        ax.set_yticklabels(["Non-ASD (0)", "ASD (1)"], fontweight="bold")
        ax.set_title(f"TabNet (Acc: {tabnet['accuracy']*100:.1f}%)", fontweight="bold", fontsize=11, color="#202B36", pad=10)
        apply_chart_theme(fig, ax)
        st.pyplot(fig)
        plt.close(fig)

    with cm_col2:
        st.write("**MLP Confusion Matrix:**")
        fig, ax = plt.subplots(figsize=(5.5, 4.2))
        sns.heatmap(
            mlp["confusion_matrix"], annot=True, fmt="d", cmap=sns.light_palette("#14243A", as_cmap=True), cbar=False, ax=ax,
            annot_kws={"size": 13, "weight": "bold"}
        )
        ax.set_xlabel(r"Predicted Class (Threshold $\geq$ 0.60)", fontweight="bold", fontsize=10)
        ax.set_ylabel("Actual Class", fontweight="bold", fontsize=10)
        ax.set_xticklabels(["Non-ASD (0)", "ASD (1)"], fontweight="bold")
        ax.set_yticklabels(["Non-ASD (0)", "ASD (1)"], fontweight="bold")
        ax.set_title(f"MLP (Acc: {mlp['accuracy']*100:.1f}%)", fontweight="bold", fontsize=11, color="#202B36", pad=10)
        apply_chart_theme(fig, ax)
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Dual ROC Curves & Feature Importance
    st.subheader("3. Receiver Operating Characteristic & Global Feature Salience")
    roc_col, feat_col = st.columns(2)

    with roc_col:
        st.write("**Combined ROC Curves:**")
        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.plot(tabnet["fpr"], tabnet["tpr"], color="#167C80", lw=2.5, label=f"TabNet (AUC = {tabnet['auc']:.3f})")
        ax.plot(mlp["fpr"], mlp["tpr"], color="#14243A", lw=2.5, linestyle="--", label=f"MLP (AUC = {mlp['auc']:.3f})")
        ax.plot([0, 1], [0, 1], color="#8899A6", linestyle="--", lw=1.5, label="Random Guess")
        ax.set_xlabel("False Positive Rate (1 - Specificity)", fontweight="bold")
        ax.set_ylabel("True Positive Rate (Sensitivity)", fontweight="bold")
        ax.set_title("Multi-Model ROC-AUC Comparison", fontweight="bold", fontsize=11, color="#202B36", pad=10)
        ax.legend(loc="lower right", frameon=True)
        apply_chart_theme(fig, ax)
        st.pyplot(fig)
        plt.close(fig)

    with feat_col:
        st.write("**TabNet Global Feature Importance Ranking:**")
        fig, ax = plt.subplots(figsize=(6, 4.5))
        top_feat = tabnet["feature_importance"].head(10).sort_values(ascending=True)
        colors = ["#5BA8AB" if i < len(top_feat) - 3 else "#167C80" for i in range(len(top_feat))]
        ax.barh(top_feat.index, top_feat.values, color=colors, edgecolor="#202B36", linewidth=0.8)
        ax.set_xlabel("Attentive Importance Score", fontweight="bold")
        ax.set_title("Top 10 Informative Clinical Features", fontweight="bold", fontsize=11, color="#202B36", pad=10)
        apply_chart_theme(fig, ax)
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Formatted Classification Reports
    st.subheader("4. Detailed Classification Reports")
    r_col1, r_col2 = st.columns(2)

    def format_report_df(rep_dict):
        rows = []
        for k, v in rep_dict.items():
            if isinstance(v, dict):
                rows.append({
                    "Class / Average": "Non-ASD (0)" if k == "0" else ("ASD (1)" if k == "1" else k.title()),
                    "Precision": f"{v['precision']:.3f}",
                    "Recall": f"{v['recall']:.3f}",
                    "F1-Score": f"{v['f1-score']:.3f}",
                    "Support": int(v['support'])
                })
        return pd.DataFrame(rows)

    with r_col1:
        st.write("**TabNet Classification Breakdown:**")
        tabnet_df = format_report_df(tabnet["classification_report"])
        st.dataframe(tabnet_df, use_container_width=True, hide_index=True)

    with r_col2:
        st.write("**MLP Classification Breakdown:**")
        mlp_df = format_report_df(mlp["classification_report"])
        st.dataframe(mlp_df, use_container_width=True, hide_index=True)

    render_disclaimer()
