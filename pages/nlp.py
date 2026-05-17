import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

_CSS = """
<style>
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
"""

def render():
    st.markdown("## NLP - Text Classification")
    st.markdown("Train and compare classifiers on real English datasets with configurable TF-IDF parameters.")

    with st.sidebar:
        st.markdown("### NLP Settings")
        dataset_name = st.selectbox("Dataset", [
            "20 Newsgroups (4 categories)",
            "20 Newsgroups (Science)",
            "20 Newsgroups (Full - 20 classes)",
        ])
        st.markdown("**TF-IDF Parameters**")
        max_features = st.select_slider("max_features", [1000, 5000, 10000, 20000, 50000], value=10000)
        ngram_max    = st.slider("ngram_range max (1=unigrams, 2=bigrams)", 1, 3, 1)
        sublinear_tf = st.checkbox("sublinear_tf (log TF)", value=True)
        st.markdown("**Classifiers to run**")
        run_nb  = st.checkbox("Naive Bayes",        value=True)
        run_svm = st.checkbox("SVM (LinearSVC)",     value=True)
        run_lr  = st.checkbox("Logistic Regression", value=True)
        run_rf  = st.checkbox("Random Forest",       value=True)

    tabs = st.tabs(["Compare all", "Single classifier", "Live predictor"])

    # -- Tab 1: Compare all classifiers ---------------------------------------
    with tabs[0]:
        st.markdown("### Compare all selected classifiers")
        if st.button("Train & Compare", type="primary", use_container_width=True):
            from algorithms.nlp_utils import load_data, build_pipeline, train_and_evaluate

            selected = []
            if run_nb:  selected.append("Naive Bayes")
            if run_svm: selected.append("SVM (LinearSVC)")
            if run_lr:  selected.append("Logistic Regression")
            if run_rf:  selected.append("Random Forest")

            if not selected:
                st.warning("Select at least one classifier.")
            else:
                with st.spinner("Loading dataset..."):
                    X_train, X_test, y_train, y_test, target_names = load_data(dataset_name)
                st.success(f"Dataset loaded: {len(X_train)} train / {len(X_test)} test samples, "
                           f"{len(target_names)} classes.")

                results = []
                prog = st.progress(0)
                for i, name in enumerate(selected):
                    with st.spinner(f"Training {name}..."):
                        pipe = build_pipeline(name, max_features=max_features,
                                              ngram_max=ngram_max, sublinear_tf=sublinear_tf)
                        metrics = train_and_evaluate(pipe, X_train, X_test, y_train, y_test)
                        metrics["classifier"] = name
                    results.append(metrics)
                    prog.progress((i + 1) / len(selected))
                prog.empty()

                st.session_state["nlp_results"] = results
                st.session_state["nlp_classes"] = target_names

        if "nlp_results" in st.session_state:
            results = st.session_state["nlp_results"]
            target_names = st.session_state["nlp_classes"]

            df = pd.DataFrame([{
                "Classifier": r["classifier"],
                "Accuracy": r["accuracy"],
                "F1 macro": r["f1_macro"],
                "Train time (s)": r["train_time"],
            } for r in results])

            fig = go.Figure()
            fig.add_trace(go.Bar(name="Accuracy", x=df["Classifier"], y=df["Accuracy"],
                                 marker_color="#818cf8"))
            fig.add_trace(go.Bar(name="F1 macro", x=df["Classifier"], y=df["F1 macro"],
                                 marker_color="#38bdf8"))
            fig.update_layout(
                barmode="group", title="Accuracy vs F1 macro",
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                font_color="#e2e8f0", height=350, yaxis=dict(range=[0, 1]),
                legend=dict(bgcolor="#1e293b"),
            )
            st.plotly_chart(fig, use_container_width=True)

            fig_t = go.Figure(go.Bar(
                x=df["Classifier"], y=df["Train time (s)"],
                marker_color="#f472b6",
                text=[f"{v:.2f}s" for v in df["Train time (s)"]],
                textposition="outside",
            ))
            fig_t.update_layout(
                title="Training time (seconds)", height=280,
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                font_color="#e2e8f0",
            )
            st.plotly_chart(fig_t, use_container_width=True)

            st.markdown("#### Confusion matrices")
            cm_cols = st.columns(min(len(results), 2))
            for idx, res in enumerate(results):
                with cm_cols[idx % 2]:
                    cm = res["confusion_matrix"]
                    fig_cm = px.imshow(
                        cm, text_auto=True,
                        x=list(target_names), y=list(target_names),
                        title=res["classifier"],
                        color_continuous_scale="Blues",
                    )
                    fig_cm.update_layout(
                        paper_bgcolor="#0f172a", font_color="#e2e8f0",
                        height=350, margin=dict(l=20, r=20, t=40, b=20),
                    )
                    st.plotly_chart(fig_cm, use_container_width=True)

    # -- Tab 2: Single classifier parameter study -----------------------------
    with tabs[1]:
        st.markdown("### Single classifier - parameter study")
        clf_choice  = st.selectbox("Classifier", ["Naive Bayes", "SVM (LinearSVC)",
                                                   "Logistic Regression", "Random Forest"])
        study_param = st.radio("Study effect of", ["max_features", "ngram_range"])

        if st.button("Run parameter study", type="primary"):
            from algorithms.nlp_utils import load_data, build_pipeline, train_and_evaluate

            with st.spinner("Loading dataset..."):
                X_train, X_test, y_train, y_test, target_names = load_data(dataset_name)

            if study_param == "max_features":
                values = [1000, 3000, 5000, 10000, 20000]
                param_label = "max_features"
            else:
                values = [1, 2, 3]
                param_label = "ngram max"

            accs, f1s = [], []
            prog2 = st.progress(0, text="Running study...")
            for i, v in enumerate(values):
                mf  = v if study_param == "max_features" else max_features
                ngr = v if study_param == "ngram_range" else ngram_max
                pipe = build_pipeline(clf_choice, max_features=mf, ngram_max=ngr,
                                      sublinear_tf=sublinear_tf)
                m = train_and_evaluate(pipe, X_train, X_test, y_train, y_test)
                accs.append(m["accuracy"]); f1s.append(m["f1_macro"])
                prog2.progress((i + 1) / len(values))
            prog2.empty()

            fig_study = go.Figure()
            fig_study.add_trace(go.Scatter(x=[str(v) for v in values], y=accs,
                                           mode="lines+markers", name="Accuracy",
                                           line=dict(color="#818cf8", width=2)))
            fig_study.add_trace(go.Scatter(x=[str(v) for v in values], y=f1s,
                                           mode="lines+markers", name="F1 macro",
                                           line=dict(color="#38bdf8", width=2)))
            fig_study.update_layout(
                title=f"{clf_choice} - effect of {param_label}",
                xaxis_title=param_label, yaxis_title="Score",
                yaxis=dict(range=[0, 1]),
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                font_color="#e2e8f0", height=340,
            )
            st.plotly_chart(fig_study, use_container_width=True)

    # -- Tab 3: Live predictor ------------------------------------------------
    with tabs[2]:
        st.markdown("### Live text predictor")
        st.markdown("Train a model, then type any English text to see the predicted category.")

        clf_live = st.selectbox("Classifier for live prediction",
                                ["SVM (LinearSVC)", "Naive Bayes",
                                 "Logistic Regression", "Random Forest"],
                                key="live_clf")

        if st.button("Train live model", type="secondary"):
            from algorithms.nlp_utils import load_data, build_pipeline
            with st.spinner("Training..."):
                X_train, X_test, y_train, y_test, target_names = load_data(dataset_name)
                pipe = build_pipeline(clf_live, max_features=max_features,
                                      ngram_max=ngram_max, sublinear_tf=sublinear_tf)
                pipe.fit(X_train, y_train)
            st.session_state["live_pipe"] = pipe
            st.session_state["live_classes"] = target_names
            st.success(f"Model ready! ({clf_live})")

        if "live_pipe" in st.session_state:
            user_text = st.text_area("Enter English text to classify:", height=150,
                                     placeholder="Type any text here...")
            if st.button("Predict", type="primary") and user_text.strip():
                pipe   = st.session_state["live_pipe"]
                labels = st.session_state["live_classes"]
                pred   = pipe.predict([user_text])[0]
                st.markdown(f"### Predicted category: **`{labels[pred]}`**")

                if hasattr(pipe.named_steps["clf"], "predict_proba"):
                    proba = pipe.predict_proba([user_text])[0]
                    fig_prob = go.Figure(go.Bar(
                        x=list(labels), y=proba,
                        marker_color=["#818cf8" if i == pred else "#334155"
                                      for i in range(len(labels))],
                    ))
                    fig_prob.update_layout(
                        title="Class probabilities", height=300,
                        paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                        font_color="#e2e8f0",
                    )
                    st.plotly_chart(fig_prob, use_container_width=True)


# -- Entry point (called by Streamlit when navigating to this page) ----------
st.set_page_config(
    page_title="NLP Classifier - AI Explorer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(_CSS, unsafe_allow_html=True)
render()
