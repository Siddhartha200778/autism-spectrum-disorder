import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from modules.theme import render_section_header, apply_chart_theme, render_disclaimer, render_html

def render():
    render_section_header(
        "Comparative Model Benchmarking Dashboard",
        "Direct performance comparison between TabNet and MLP neural architectures on identical hold-out test data.",
        badge="HEAD-TO-HEAD EVALUATION"
    )

    if "models_result" not in st.session_state:
        st.info("💡 The models are initializing on the benchmark dataset...")
        return

    models = st.session_state["models_result"]
    tabnet = models["tabnet"]
    mlp = models["mlp"]

    # Comparative Summary Cards
    st.subheader("1. Core Performance Metrics Comparison")
    
    col_tab, col_mlp = st.columns(2)
    with col_tab:
        render_html("""
        <div class="med-card" style="border-top: 4px solid #167C80;">
            <div class="med-card-header">
                <div class="med-card-icon">🧠</div>
                <span class="pill-badge pill-blue">Attentive Architecture</span>
            </div>
            <div class="med-card-title">TabNet Performance</div>
        </div>
        """)
        c1, c2 = st.columns(2)
        c1.metric("Accuracy", f"{tabnet['accuracy'] * 100:.2f}%")
        c2.metric("F1-Score", f"{tabnet['f1'] * 100:.2f}%")
        c3, c4 = st.columns(2)
        c3.metric("Precision", f"{tabnet['precision'] * 100:.2f}%")
        c4.metric("Recall", f"{tabnet['recall'] * 100:.2f}%")

    with col_mlp:
        render_html("""
        <div class="med-card" style="border-top: 4px solid #167C80;">
            <div class="med-card-header">
                <div class="med-card-icon" style="color:#14243A; font-weight:700; font-size:11px;">MLP</div>
                <span class="pill-badge pill-purple">Feedforward Network</span>
            </div>
            <div class="med-card-title">MLP Network Performance</div>
        </div>
        """)
        c1, c2 = st.columns(2)
        c1.metric("Accuracy", f"{mlp['accuracy'] * 100:.2f}%")
        c2.metric("F1-Score", f"{mlp['f1'] * 100:.2f}%")
        c3, c4 = st.columns(2)
        c3.metric("Precision", f"{mlp['precision'] * 100:.2f}%")
        c4.metric("Recall", f"{mlp['recall'] * 100:.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Grouped Bar Chart
    st.subheader("2. Side-by-Side Metric Visualization")

    metrics_df = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1 Score"],
        "TabNet": [tabnet["accuracy"] * 100, tabnet["precision"] * 100, tabnet["recall"] * 100, tabnet["f1"] * 100],
        "MLP": [mlp["accuracy"] * 100, mlp["precision"] * 100, mlp["recall"] * 100, mlp["f1"] * 100]
    })

    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    x = np.arange(len(metrics_df))
    width = 0.35

    rects1 = ax.bar(x - width/2, metrics_df["TabNet"], width, label="TabNet", color="#167C80", edgecolor="#202B36", linewidth=1.2)
    rects2 = ax.bar(x + width/2, metrics_df["MLP"], width, label="MLP Neural Net", color="#14243A", edgecolor="#202B36", linewidth=1.2)

    ax.set_ylabel("Score (%)", fontweight="bold")
    ax.set_title("TabNet vs MLP Performance Comparison on Pediatric Test Cohort", fontsize=11, fontweight="bold", color="#202B36", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_df["Metric"], fontweight="bold", fontsize=10)
    ax.set_ylim(0, 115)
    ax.legend(frameon=True, loc="upper right")

    # Add direct percentage labels on bars
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#167C80')
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#14243A')

    apply_chart_theme(fig, ax)
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)

    # Detailed Comparison Table
    st.subheader("3. Comprehensive Comparison Table")
    comp_table = pd.DataFrame({
        "Evaluation Dimension": [
            "Test Set Accuracy",
            "Precision (Positive Predictive Value)",
            "Recall (Sensitivity)",
            "F1-Score (Harmonic Mean)",
            "ROC Area Under Curve (AUC)",
            "Feature Interpretability",
            "Training Convergence",
            "Invariance to Noise",
            "Clinical Deployment Suitability"
        ],
        "TabNet (Attentive Tabular)": [
            f"{tabnet['accuracy'] * 100:.2f}%",
            f"{tabnet['precision'] * 100:.2f}%",
            f"{tabnet['recall'] * 100:.2f}%",
            f"{tabnet['f1'] * 100:.2f}%",
            f"{tabnet['auc']:.3f}",
            "High (Explicit Sparse Attention Masks)",
            "Multi-epoch Adam with early stopping",
            "High (Robust tabular inductive bias)",
            "Ideal for Explainable Decision Support"
        ],
        "MLP (Multi-Layer Perceptron)": [
            f"{mlp['accuracy'] * 100:.2f}%",
            f"{mlp['precision'] * 100:.2f}%",
            f"{mlp['recall'] * 100:.2f}%",
            f"{mlp['f1'] * 100:.2f}%",
            f"{mlp['auc']:.3f}",
            "Moderate (Post-hoc perturbation required)",
            f"Rapid ({mlp['iterations']} iterations)",
            "Moderate (Controlled by L2 weight decay)",
            "Ideal for High-Throughput Batch Triage"
        ]
    })
    st.dataframe(comp_table, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("4. Clinical Research Insights")
    st.markdown("""- **Clinical Interpretability:** TabNet delivers direct feature-level importance attribution via sparse attention. In pediatric medical settings, explainability is as critical as raw accuracy because clinicians must justify screening referrals to caregivers.
- **Complementary Ensemble Potential:** The MLP model excels at capturing dense non-linear interactions across the engineered Q-Chat domains (`AQ10`, `A_domain`, `B_domain`), while TabNet provides granular item-level tracking. Utilizing both models in tandem maximizes screening confidence.""")

    render_disclaimer()
