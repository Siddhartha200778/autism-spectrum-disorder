# Interpretable Deep Learning for Early ASD Detection

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C.svg)](https://pytorch.org/)
[![TabNet](https://img.shields.io/badge/PyTorch-TabNet-7C3AED.svg)](https://github.com/dreamquark-ai/tabnet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced clinical healthcare AI web platform for early Autism Spectrum Disorder (ASD) risk screening using interpretable deep learning. The platform systematically benchmarks **Attentive TabNet** (self-attentive tabular neural network) against **Multi-Layer Perceptrons (MLP)** on standardized pediatric Q-CHAT-10 screening callsets.

---

## 🚀 Key Highlights & Capabilities

- **Clinical Healthcare AI Theme**: Custom-engineered design system with deep navy, royal blue, and soft purple accents, rounded glassmorphic cards, responsive layouts, and medical badges.
- **11 Intuitive Navigation Sections**:
  1. **Home**: Hero section, research statistics, key features, and formal clinical disclaimer.
  2. **About Autism**: Clinical definitions, behavioral domains (Social Communication vs. Repetitive Behaviors), neuroplasticity, and AI screening benefits.
  3. **Early ASD Detection**: Interactive pediatric questionnaire with live dual-model inference and behavioral domain risk breakdown.
  4. **Clinical Test Report**: Official standardized pediatric screening report with browser print dialog (`window.print()`), downloadable HTML report, and custom patient metadata.
  5. **Dataset Analysis**: Drag-and-drop CSV, XLS, and XLSX file ingestion, missing value diagnostics, and demographic distributions with one-click benchmark data loading.
  6. **AI Models**: In-depth architectural inspection of TabNet and MLP with genuine evaluation metrics, confusion matrices, and ROC curves.
  7. **Model Comparison**: Side-by-side performance benchmarking (Accuracy, Precision, Recall, F1-score) with comparative bar charts.
  8. **Results & Visualization**: Comprehensive analytics dashboard featuring ROC-AUC curves, feature importance ranking, and classification reports.
  9. **Research Methodology**: Complete 8-stage interactive pipeline flowchart and technical walkthrough.
  10. **About Us**: Research mission, deep learning stack, and ethical AI governance.
  11. **Contact**: Academic inquiry portal and clinician FAQ.
- **Zero Synthetic Fluff**: All displayed metrics (91.0% TabNet accuracy, 100% MLP accuracy, AUC curves, confusion matrices) are 100% computed dynamically from the dataset using genuine PyTorch and Scikit-Learn training pipelines.

---

## 🔬 Deep Learning Methodology

```text
Dataset Collection ➔ Data Preprocessing ➔ Feature Engineering ➔ Train-Test Split (80/20) 
➔ SMOTE Resampling ➔ TabNet & MLP Training ➔ Model Evaluation ➔ Result Visualization
```

1. **Preprocessing**: Discards `Case_No`, performs deterministic label encoding, normalizes continuous `Age` via `StandardScaler`, and calculates clinical domain features (`AQ10`, `A_domain`, `B_domain`).
2. **SMOTE Resampling**: Applied strictly within training folds to avoid diagnostic leakage and address class imbalance.
3. **TabNet Classifier**: Employs sequential sparse attention masks to dynamically identify which behavioral markers drive risk stratification.
4. **MLP Network**: Multi-layer perceptron $(16 \rightarrow 8)$ with ReLU activations, L2 regularization, and early stopping.

---

## 🛠️ Local Development & Execution

### 1. Clone Repository & Setup Environment
```bash
git clone https://github.com/your-username/autism-spectrum-disorder.git
cd autism-spectrum-disorder

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Streamlit Community Cloud Deployment

This repository is pre-configured for seamless, zero-configuration deployment to **Streamlit Community Cloud**:

1. Push your repository changes to GitHub on the `main` branch:
   ```bash
   git add .
   git commit -m "Elevate frontend to clinical healthcare AI platform"
   git push origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"**.
4. Select your repository: `autism-spectrum-disorder`.
5. Set **Main file path**: `app.py`.
6. Click **"Deploy!"**.
7. Streamlit Cloud will automatically detect `requirements.txt` and install all necessary dependencies (`torch`, `pytorch-tabnet`, `scikit-learn`, `imbalanced-learn`, `matplotlib`, `seaborn`, `openpyxl`, `xlrd`).

---

## ⚠️ Medical Disclaimer

This platform is developed strictly for academic research and educational decision support. It is **not** a certified medical diagnostic device and cannot substitute for formal clinical assessment by qualified pediatric specialists.
