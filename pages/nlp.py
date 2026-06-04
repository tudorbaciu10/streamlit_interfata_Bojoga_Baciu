import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from utils.i18n import t, lang_switcher_sidebar

_CSS = """
<style>
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
"""


@st.cache_data(show_spinner=False)
def _load_dataset(dataset_name):
    """Cache dataset so it is downloaded only once."""
    from algorithms.nlp_utils import load_data
    return load_data(dataset_name)


def render():
    st.markdown(f"## {t('nlp_title')}")
    st.markdown(t("nlp_subtitle"))

    with st.sidebar:
        st.markdown(f"### {t('nlp_sidebar')}")
        dataset_name = st.selectbox(t("nlp_dataset"), [
            "20 Newsgroups (4 categories)",
            "20 Newsgroups (Science)",
            "20 Newsgroups (Full - 20 classes)",
        ])
        st.markdown(f"**{t('nlp_tfidf_hdr')}**")
        max_features = st.select_slider("max_features",
                                        [1000, 5000, 10000, 20000, 50000], value=10000)
        ngram_max    = st.slider("ngram_range max (1=unigrams, 2=bigrams)", 1, 3, 1)
        sublinear_tf = st.checkbox("sublinear_tf (log TF)", value=True)
        st.markdown(f"**{t('nlp_clf_hdr')}**")
        run_nb   = st.checkbox("Naive Bayes",        value=True)
        run_svm  = st.checkbox("SVM (LinearSVC)",    value=True)
        run_lr   = st.checkbox("Logistic Regression", value=True)
        run_rf   = st.checkbox("Random Forest",      value=True)
        run_dict = st.checkbox(t("nlp_dict_clf"),    value=True)

    lang_switcher_sidebar("nlp")

    tabs = st.tabs([
        t("nlp_tab_compare"),
        t("nlp_tab_single"),
        t("nlp_tab_live"),
        t("nlp_tab_dicts"),
    ])

    # -- Tab 1: Compare all ---------------------------------------------------
    with tabs[0]:
        st.markdown(f"### {t('nlp_compare_hdr')}")
        if st.button(t("nlp_run_btn"), type="primary", use_container_width=True):
            from algorithms.nlp_utils import (build_pipeline, train_and_evaluate,
                                              dict_train_and_evaluate)

            selected_ml = []
            if run_nb:  selected_ml.append("Naive Bayes")
            if run_svm: selected_ml.append("SVM (LinearSVC)")
            if run_lr:  selected_ml.append("Logistic Regression")
            if run_rf:  selected_ml.append("Random Forest")

            if not selected_ml and not run_dict:
                st.warning(t("nlp_no_clf"))
            else:
                try:
                    with st.spinner("Se descarcă / încarcă setul de date (prima rulare poate dura ~30s)..."):
                        X_train, X_test, y_train, y_test, target_names = _load_dataset(dataset_name)
                    st.success(t("nlp_loaded",
                                 train=len(X_train), test=len(X_test), cls=len(target_names)))

                    results = []
                    total   = len(selected_ml) + (1 if run_dict else 0)
                    prog    = st.progress(0)

                    for i, name in enumerate(selected_ml):
                        with st.spinner(f"Antrenare {name} ({i+1}/{total})..."):
                            pipe    = build_pipeline(name, max_features=max_features,
                                                     ngram_max=ngram_max, sublinear_tf=sublinear_tf)
                            metrics = train_and_evaluate(pipe, X_train, X_test, y_train, y_test)
                            metrics["classifier"] = name
                        results.append(metrics)
                        prog.progress((i + 1) / total)

                    if run_dict:
                        with st.spinner(f"Rulare {t('nlp_dict_clf')} ({total}/{total})..."):
                            metrics = dict_train_and_evaluate(
                                X_train, X_test, y_train, y_test, target_names)
                            metrics["classifier"] = t("nlp_dict_clf")
                        results.append(metrics)
                        prog.progress(1.0)

                    prog.empty()
                    st.session_state["nlp_results"] = results
                    st.session_state["nlp_classes"] = target_names
                except Exception as exc:
                    st.error(f"Eroare la antrenare: {exc}")
                    st.exception(exc)

        if "nlp_results" in st.session_state:
            results      = st.session_state["nlp_results"]
            target_names = st.session_state["nlp_classes"]

            df = pd.DataFrame([{
                "Classifier":     r["classifier"],
                "Accuracy":       r["accuracy"],
                "F1 macro":       r["f1_macro"],
                "Train time (s)": r["train_time"],
            } for r in results])

            fig = go.Figure()
            fig.add_trace(go.Bar(name="Accuracy", x=df["Classifier"], y=df["Accuracy"],
                                 marker_color="#818cf8"))
            fig.add_trace(go.Bar(name="F1 macro", x=df["Classifier"], y=df["F1 macro"],
                                 marker_color="#38bdf8"))
            fig.update_layout(
                barmode="group", title=t("nlp_acc_f1_title"),
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
                title=t("nlp_time_title"), height=280,
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b", font_color="#e2e8f0",
            )
            st.plotly_chart(fig_t, use_container_width=True)

            clf_colors = ["#818cf8", "#38bdf8", "#34d399", "#fb923c",
                          "#f472b6", "#a78bfa", "#fbbf24"]
            fig_perf = go.Figure()
            for i, r in enumerate(results):
                fig_perf.add_trace(go.Scatter(
                    x=[r["train_time"]], y=[r["accuracy"]],
                    mode="markers+text",
                    marker=dict(size=18, color=clf_colors[i % len(clf_colors)],
                                line=dict(color="#e2e8f0", width=1)),
                    text=[r["classifier"]], textposition="top center",
                    name=r["classifier"],
                ))
            fig_perf.update_layout(
                title=t("nlp_perf_title"),
                xaxis_title="Training time (s)", yaxis_title="Accuracy",
                yaxis=dict(range=[0, 1.05]),
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                font_color="#e2e8f0", height=360, legend=dict(bgcolor="#1e293b"),
            )
            st.plotly_chart(fig_perf, use_container_width=True)

            st.markdown(f"#### {t('nlp_cm_hdr')}")
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
        st.markdown(f"### {t('nlp_single_hdr')}")
        clf_choice  = st.selectbox("Classifier",
                                   ["Naive Bayes", "SVM (LinearSVC)",
                                    "Logistic Regression", "Random Forest"])
        study_param = st.radio(t("nlp_study_effect"), ["max_features", "ngram_range"])

        if st.button(t("nlp_study_btn"), type="primary"):
            from algorithms.nlp_utils import build_pipeline, train_and_evaluate

            with st.spinner("Se încarcă setul de date..."):
                X_train, X_test, y_train, y_test, target_names = _load_dataset(dataset_name)

            values      = ([1000, 3000, 5000, 10000, 20000] if study_param == "max_features"
                           else [1, 2, 3])
            param_label = study_param
            accs, f1s   = [], []
            prog2       = st.progress(0, text="Running study...")
            for i, v in enumerate(values):
                mf  = v if study_param == "max_features" else max_features
                ngr = v if study_param == "ngram_range"  else ngram_max
                pipe = build_pipeline(clf_choice, max_features=mf, ngram_max=ngr,
                                      sublinear_tf=sublinear_tf)
                m = train_and_evaluate(pipe, X_train, X_test, y_train, y_test)
                accs.append(m["accuracy"])
                f1s.append(m["f1_macro"])
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
                title=f"{clf_choice} — {t('nlp_study_effect')} {param_label}",
                xaxis_title=param_label, yaxis_title="Score",
                yaxis=dict(range=[0, 1]),
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                font_color="#e2e8f0", height=340,
            )
            st.plotly_chart(fig_study, use_container_width=True)

    # -- Tab 3: Live predictor ------------------------------------------------
    with tabs[2]:
        st.markdown(f"### {t('nlp_live_hdr')}")
        st.markdown(t("nlp_live_desc"))

        clf_live_options = ["SVM (LinearSVC)", "Naive Bayes",
                            "Logistic Regression", "Random Forest",
                            t("nlp_dict_clf")]
        clf_live = st.selectbox("Classifier", clf_live_options, key="live_clf")

        if st.button(t("nlp_train_btn"), type="secondary"):
            from algorithms.nlp_utils import (build_pipeline, dict_train_and_evaluate)
            try:
                with st.spinner("Se încarcă setul de date..."):
                    X_train, X_test, y_train, y_test, target_names = _load_dataset(dataset_name)
                with st.spinner(f"Antrenare {clf_live}..."):
                    if clf_live == t("nlp_dict_clf"):
                        res = dict_train_and_evaluate(
                            X_train, X_test, y_train, y_test, target_names)
                        st.session_state["live_model"] = res["clf"]
                    else:
                        pipe = build_pipeline(clf_live, max_features=max_features,
                                              ngram_max=ngram_max, sublinear_tf=sublinear_tf)
                        pipe.fit(X_train, y_train)
                        st.session_state["live_model"] = pipe
                    st.session_state["live_classes"] = target_names
                st.success(t("nlp_model_ready", clf=clf_live))
            except Exception as exc:
                st.error(f"Eroare: {exc}")
                st.exception(exc)

        if "live_model" in st.session_state:
            user_text = st.text_area(t("nlp_text_label"), height=150,
                                     placeholder=t("nlp_text_ph"))
            if st.button(t("nlp_predict_btn"), type="primary") and user_text.strip():
                model  = st.session_state["live_model"]
                labels = st.session_state["live_classes"]
                pred   = model.predict([user_text])[0]
                st.markdown(f"### {t('nlp_predicted')} **`{labels[pred]}`**")

                if hasattr(model, "predict_proba"):
                    proba    = model.predict_proba([user_text])[0]
                    fig_prob = go.Figure(go.Bar(
                        x=list(labels), y=proba,
                        marker_color=["#818cf8" if i == pred else "#334155"
                                      for i in range(len(labels))],
                    ))
                    fig_prob.update_layout(
                        title=t("nlp_proba_title"), height=300,
                        paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                        font_color="#e2e8f0",
                    )
                    st.plotly_chart(fig_prob, use_container_width=True)

    # -- Tab 4: Keyword dictionaries ------------------------------------------
    with tabs[3]:
        st.markdown(f"### {t('nlp_dicts_hdr')}")
        st.markdown(t("nlp_dicts_desc"))

        from algorithms.nlp_utils import KEYWORD_DICTS, DATASETS

        cfg         = DATASETS[dataset_name]
        active_cats = cfg["categories"] or list(KEYWORD_DICTS.keys())

        for cat in active_cats:
            words = KEYWORD_DICTS.get(cat, [])
            with st.expander(f"{cat}  ({len(words)} keywords)", expanded=False):
                st.write(", ".join(sorted(words)))

        total_words = sum(len(KEYWORD_DICTS.get(c, [])) for c in active_cats)
        st.caption(t("nlp_dicts_footer", n=len(active_cats), total=total_words))


# -- Entry point --------------------------------------------------------------
st.set_page_config(
    page_title="NLP Classifier - AI Explorer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(_CSS, unsafe_allow_html=True)
render()
