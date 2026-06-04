import streamlit as st
from utils.i18n import t, lang_switcher_sidebar

_CSS = """
<style>
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
"""

st.set_page_config(
    page_title="Echipa - AI Explorer",
    page_icon="👥",
    layout="centered",
    initial_sidebar_state="auto",
)
st.markdown(_CSS, unsafe_allow_html=True)

lang_switcher_sidebar("echipa")

st.markdown(f"# {t('echipa_title')}")
st.divider()

col_label, col_name = st.columns([1, 2])
with col_label:
    st.markdown(f"### {t('echipa_team_label')}")
with col_name:
    st.markdown("## Just Here For Money")

st.divider()

info_l, info_r = st.columns(2)
with info_l:
    st.markdown(f"**{t('echipa_fac_label')}**")
    st.markdown(t("echipa_fac_val"))
    st.markdown(f"**{t('echipa_univ_label')}**")
    st.markdown(t("echipa_univ_val"))
    st.markdown(f"**{t('echipa_spec_label')}**")
    st.markdown(t("echipa_spec_val"))

with info_r:
    st.markdown(f"**{t('echipa_year_label')}**")
    st.markdown(t("echipa_year_val"))
    st.markdown(f"**{t('echipa_subj_label')}**")
    st.markdown(t("echipa_subj_val"))
    st.markdown(f"**{t('echipa_prof_label')}**")
    st.markdown(t("echipa_prof_val"))

st.divider()
st.markdown(f"### {t('echipa_members')}")

m1, m2 = st.columns(2)
with m1:
    with st.container(border=True):
        st.markdown("### Bojoga Andrei")
        st.markdown(t("echipa_student"))
        st.markdown(t("echipa_fiesc"))

with m2:
    with st.container(border=True):
        st.markdown("### Baciu Tudor")
        st.markdown(t("echipa_student"))
        st.markdown(t("echipa_fiesc"))

st.divider()
st.markdown(f"### {t('echipa_about')}")
st.markdown(t("echipa_about_text"))
