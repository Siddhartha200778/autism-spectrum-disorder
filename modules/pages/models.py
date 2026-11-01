import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from modules.theme import render_section_header, apply_chart_theme, render_disclaimer

def render():
    render_section_header(
        "AI Architecture Deep Dive",
        "Detailed inspection of the Attentive TabNet tabular learner and Multi-Layer Perceptron neural network.",
        badge="DEEP LEARNING ARCHITECTURES"
    )

    if "models_result" not in st.session_state or "prepared_data" not in st.session_state:
        st.info("💡 The models are initializing on the benchmark dataset...")
        return

    models = st.session_state["models_result"]
    tabnet_res = models["tabnet"]
    mlp_res = models["mlp"]

    tab_choice = st.radio("Select Model Architecture to Inspect:", ["TabNet (Attentive Tabular Learning)", "MLP Neural Network (Multi-Layer Perceptron)"], horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if "TabNet" in tab_choice:
        # TabNet Section
        st.markdown("""
        <div class="med-card" style="border-left: 5px solid #1D4ED8;">
            <div class="med-card-title" style="font-size: 1.3rem; color: #0A192F;">
                TabNet: Attentive Interpretable Tabular Learning
            </div>
            <div class="med-card-body" style="font-size: 0.98rem; line-height: 1.6;">
                <strong>TabNet</strong> is a state-of-the-art deep learning architecture engineered specifically for tabular clinical datasets. 
                Unlike standard feed-forward networks, TabNet utilizes a sequential multi-step attention mechanism with <em>Sparsemax</em> masking to select salient features at each decision step. 
                This provides intrinsic interpretability, enabling researchers to quantify precisely how much weight each Q-Chat behavioral question carries during diagnosis.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("TabNet Evaluation Metrics (Actual Test Set Results)")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Accuracy", f"{tabnet_res['accuracy'] * 100:.2f}%")
        m2.metric("Precision", f"{tabnet_res['precision'] * 100:.2f}%")
        m3.metric("Recall", f"{tabnet_res['recall'] * 100:.2f}%")
        m4.metric("F1-Score", f"{tabnet_res['f1'] * 100:.2f}%")

        st.markdown("<br>", unsafe_allow_html=True)
        col_fig1, col_fig2 = st.columns(2)

        with col_fig1:
            st.subheader("TabNet Feature Importance")
            fig, ax = plt.subplots(figsize=(6.5, 5))
            importance = tabnet_res["feature_importance"].sort_values(ascending=True)
            # Take top 10 features if many
            top_importance = importance.tail(12)
            colors = ["#93C5FD" if i < len(top_importance) - 3 else "#1D4ED8" for i in range(len(top_importance))]
            ax.barh(top_importance.index, top_importance.values, color=colors, edgecolor="#0A192F", linewidth=0.8)
            ax.set_title("TabNet Feature Salience (Top Contributors)", fontsize=11, fontweight="bold", color="#0A192F", pad=12)
            ax.set_xlabel("Relative Importance Score", fontweight="bold")
            apply_chart_theme(fig, ax)
            st.pyplot(fig)
            plt.close(fig)

        with col_fig2:
            st.subheader("TabNet Confusion Matrix")
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(
                tabnet_res["confusion_matrix"],
                annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                annot_kws={"size": 14, "weight": "bold"}
            )
            ax.set_xlabel("Predicted Label", fontweight="bold", fontsize=10, labelpad=8)
            ax.set_ylabel("Actual Label", fontweight="bold", fontsize=10, labelpad=8)
            ax.set_xticklabels(["Non-ASD (0)", "ASD (1)"], fontweight="bold")
            ax.set_yticklabels(["Non-ASD (0)", "ASD (1)"], fontweight="bold")
            ax.set_title("TabNet Confusion Matrix", fontsize=11, fontweight="bold", color="#0A192F", pad=12)
            apply_chart_theme(fig, ax)
            st.pyplot(fig)
            plt.close(fig)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("TabNet Hyperparameter Configuration")
        st.markdown(r"""
        - **Decision Steps ($N_{steps}$):** 5
        - **Feature Dimension ($N_d$) / Attention Dimension ($N_a$):** 16 / 16
        - **Sparsity Regularization Factor ($\lambda_{sparse}$):** $1 \times 10^{-4}$
        - **Gamma ($\gamma$):** 1.5
        - **Optimizer:** Adam (Initial Learning Rate = 0.02)
        - **Batch Size / Virtual Batch Size:** 256 / 128
        """)

    else:
        # MLP Section
        st.markdown("""
        <div class="med-card" style="border-left: 5px solid #7C3AED;">
            <div class="med-card-title" style="font-size: 1.3rem; color: #0A192F;">
                Multi-Layer Perceptron (MLP) Neural Network
            </div>
            <div class="med-card-body" style="font-size: 0.98rem; line-height: 1.6;">
                The <strong>Multi-Layer Perceptron (MLP)</strong> is a deep feed-forward artificial neural network architecture with two dense hidden layers (16 and 8 neurons). 
                Equipped with ReLU non-linear activations, L2 regularization ($\alpha = 0.1$), and early stopping validation monitoring, the MLP effectively learns high-level non-linear feature representations for robust developmental trait classification.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("MLP Evaluation Metrics (Actual Test Set Results)")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Accuracy", f"{mlp_res['accuracy'] * 100:.2f}%")
        m2.metric("Precision", f"{mlp_res['precision'] * 100:.2f}%")
        m3.metric("Recall", f"{mlp_res['recall'] * 100:.2f}%")
        m4.metric("F1-Score", f"{mlp_res['f1'] * 100:.2f}%")

        st.markdown("<br>", unsafe_allow_html=True)
        col_fig1, col_fig2 = st.columns(2)

        with col_fig1:
            st.subheader(f"MLP ROC Curve (AUC = {mlp_res['auc']:.3f})")
            fig, ax = plt.subplots(figsize=(6.5, 5))
            ax.plot(mlp_res["fpr"], mlp_res["tpr"], color="#7C3AED", lw=2.5, label=f"MLP (AUC = {mlp_res['auc']:.3f})")
            ax.plot([0, 1], [0, 1], color="#94A3B8", linestyle="--", lw=1.5, label="Chance Level")
            ax.set_title("Receiver Operating Characteristic (ROC)", fontsize=11, fontweight="bold", color="#0A192F", pad=12)
            ax.set_xlabel("False Positive Rate", fontweight="bold")
            ax.set_ylabel("True Positive Rate", fontweight="bold")
            ax.legend(loc="lower right", frameon=True)
            apply_chart_theme(fig, ax)
            st.pyplot(fig)
            plt.close(fig)

        with col_fig2:
            st.subheader("MLP Confusion Matrix")
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(
                mlp_res["confusion_matrix"],
                annot=True, fmt="d", cmap="Purples", cbar=False, ax=ax,
                annot_kws={"size": 14, "weight": "bold"}
            )
            ax.set_xlabel(r"Predicted Label (Threshold $\ge$ 0.60)", fontweight="bold", fontsize=10, labelpad=8)
            ax.set_ylabel("Actual Label", fontweight="bold", fontsize=10, labelpad=8)
            ax.set_xticklabels(["Non-ASD (0)", "ASD (1)"], fontweight="bold")
            ax.set_yticklabels(["Non-ASD (0)", "ASD (1)"], fontweight="bold")
            ax.set_title("MLP Confusion Matrix", fontsize=11, fontweight="bold", color="#0A192F", pad=12)
            apply_chart_theme(fig, ax)
            st.pyplot(fig)
            plt.close(fig)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("MLP Training Dynamics")
        st.markdown(f"""
        - **Hidden Layers:** $(16, 8)$ neurons
        - **Activation Function:** Rectified Linear Unit (ReLU)
        - **L2 Regularization Penalty ($\alpha$):** $0.1$
        - **Decision Threshold:** $0.60$
        - **Early Stopping:** Active (Validation fraction = 0.20)
        - **Convergence Epoch:** Reached optimum in **{mlp_res['iterations']} iterations**
        """)

    render_disclaimer()
