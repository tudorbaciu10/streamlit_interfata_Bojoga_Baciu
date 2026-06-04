import streamlit as st
import uuid
from utils.i18n import t, lang_switcher_sidebar

st.set_page_config(page_title="Task Manager", page_icon="✅", layout="centered")

lang_switcher_sidebar("tm")

st.title(t("tm_title"))

if "tasks" not in st.session_state:
    st.session_state.tasks = []

with st.form("form_adaugare", clear_on_submit=True):
    st.markdown(f"**{t('tm_form_header')}**")
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        text_nou = st.text_input(t("tm_field_label"), placeholder=t("tm_placeholder"))
    with col_btn:
        st.markdown("&nbsp;", unsafe_allow_html=True)
        adaugat = st.form_submit_button(t("tm_add_btn"), use_container_width=True)

if adaugat:
    if text_nou.strip():
        st.session_state.tasks.append({
            "id":   str(uuid.uuid4()),
            "text": text_nou.strip(),
            "done": False,
        })
    else:
        st.warning(t("tm_empty_warning"))

st.divider()

if not st.session_state.tasks:
    st.info(t("tm_no_tasks"))
else:
    total      = len(st.session_state.tasks)
    done_count = sum(1 for task in st.session_state.tasks if task["done"])
    st.markdown(f"**{t('tm_progress', done=done_count, total=total)}**")
    st.progress(done_count / total)
    st.markdown("")

    to_delete = None

    for i, task in enumerate(st.session_state.tasks):
        col_cb, col_text, col_del = st.columns([1, 10, 1])

        with col_cb:
            done = st.checkbox("", value=task["done"], key=f"cb_{task['id']}")
            st.session_state.tasks[i]["done"] = done

        with col_text:
            if done:
                st.markdown(
                    f"<span style='text-decoration:line-through;color:#64748b'>"
                    f"{task['text']}</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(task["text"])

        with col_del:
            if st.button("✕", key=f"del_{task['id']}"):
                to_delete = i

    if to_delete is not None:
        st.session_state.tasks.pop(to_delete)
        st.rerun()
