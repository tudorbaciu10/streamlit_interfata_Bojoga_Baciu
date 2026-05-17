import streamlit as st

st.set_page_config(
    page_title="AI Algorithm Explorer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<h1 style="background:linear-gradient(135deg,#818cf8,#38bdf8);'
    '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
    'font-size:2.6rem;font-weight:900">AI Algorithm Explorer</h1>',
    unsafe_allow_html=True,
)
st.markdown("### Explore, parametrize and compare classic AI algorithms - interactively.")
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### TSP - Travelling Salesman Problem")
    st.markdown("""
Compare **5 algorithms** head-to-head on identical city layouts:

| Algorithm | Strategy | Finds Optimal? |
|---|---|---|
| **BKT** Backtracking | Exhaustive + B&B pruning | Yes - Always |
| **NN** Nearest Neighbour | Greedy constructive | No - Heuristic |
| **HC** Hill Climbing | Local search, 2-opt | No - Local opt. |
| **SA** Simulated Annealing | Probabilistic escape | Near-optimal |
| **GA** Genetic Algorithm | Evolutionary, OX crossover | Near-optimal |

**Features:** interactive city map, cost comparison bar chart, convergence curves, parameter sliders.
    """)

with col2:
    st.markdown("#### NLP - Text Classification")
    st.markdown("""
Train and compare **4 classifiers** on real English datasets:

| Classifier | Key Strength |
|---|---|
| Naive Bayes | Speed, probabilistic |
| SVM (LinearSVC) | High accuracy on text |
| Logistic Regression | Interpretable weights |
| Random Forest | Ensemble, robust |

**Datasets:** 20 Newsgroups (4 topics / science / full 20 classes)

**Features:** TF-IDF parametrization (ngram, max_features), confusion matrix heatmap,
classifier comparison bar chart, live text predictor.
    """)

st.markdown("---")
st.info("Use the **sidebar navigation** to switch between TSP and NLP pages.")

with st.expander("About this app"):
    st.markdown("""
This application was built for the **Artificial Intelligence** course (Year III, Sem II, 2025-2026).

It covers algorithms from Labs 04 (BKT, NN), 08 (SA), 09 (GA), 10 (NLP), plus Hill Climbing (Lab 03).

**Tech stack:** Python · Streamlit · scikit-learn · Plotly · Matplotlib
    """)
