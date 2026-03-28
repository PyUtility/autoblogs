# -*- coding: utf-8 -*-
"""
Draft Editor Page

Renders the review and editing UI for a generated blog post draft.
Provides inline editing, markdown preview, save-to-file and browser
download capabilities.
"""

# --- standard library ---
import os

# --- third-party ---
import streamlit as st

# --- local / internal ---
from autoblogs.manager.content import ContentManager
from autoblogs.ui.components.render import render_page


def review() -> None:
    """
    Render the Draft Editor Page.

    Displays the generated draft with word count, token, and latency
    metrics. Provides edit/preview toggle, save-to-file form, and a
    direct browser download button.

    :rtype:  None
    :return: None — renders Streamlit UI components in place.
    """
    st.title("✍ Draft Editor")
    st.divider()

    if "response" not in st.session_state or st.session_state["response"] is None:
        st.info("No content generated yet. Go to Create Content to generate a post.")
        return

    response = st.session_state["response"]
    topic    = st.session_state.get("topic", "Untitled")

    st.subheader(f"Topic: {topic}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Words",        response.word_count)
    col2.metric("Total Tokens", response.total_tokens)
    col3.metric("Latency (s)",  f"{response.latency:.2f}")

    st.divider()

    if "preview_mode" not in st.session_state:
        st.session_state["preview_mode"] = False

    col_edit, col_preview = st.columns([1, 1])
    with col_edit:
        if st.button("Edit", use_container_width = True, type = "secondary"):
            st.session_state["preview_mode"] = False
    with col_preview:
        if st.button("Preview", use_container_width = True, type = "primary"):
            st.session_state["preview_mode"] = True

    if st.session_state["preview_mode"]:
        st.markdown(st.session_state.get("draft", response.raw_response or ""))
    else:
        draft = st.text_area(
            "Edit Draft",
            value  = st.session_state.get("draft", response.raw_response or ""),
            height = 600,
            key    = "draft_editor"
        )
        st.session_state["draft"] = draft

    st.divider()

    s      = st.session_state.get("settings", {})
    outdir = s.get("outdir", os.getenv("CONTENT_OUTPUT_DIR", "output"))

    tab_save, tab_download = st.tabs(["Save to File", "Download"])

    with tab_save:
        with st.form("save_draft"):
            filename = st.text_input(
                "Output Filename", placeholder = "e.g. linear-regression.md"
            )
            save = st.form_submit_button("Save to File", type = "primary")

        if save and filename.strip():
            filepath = os.path.join(outdir, filename.strip())
            manager  = ContentManager(outdir = outdir, context = "base.txt.jinja")
            try:
                manager.writefile(
                    content  = st.session_state.get("draft", response.raw_response or ""),
                    filename = filepath
                )
                st.success(f"Saved to `{filepath}`.")
            except AssertionError:
                st.error(f"File already exists: `{filepath}`.")
            except Exception as e:
                st.error(f"Failed to save: {e}")

    with tab_download:
        draft_content = st.session_state.get("draft", response.raw_response or "")
        dl_filename   = st.text_input(
            "Download Filename",
            placeholder = "e.g. linear-regression.md",
            key         = "dl_filename"
        )
        st.download_button(
            label               = "Download File",
            data                = draft_content,
            file_name           = dl_filename.strip() if dl_filename.strip() else "draft.md",
            mime                = "text/markdown",
            type                = "primary",
            use_container_width = True
        )


render_page(review)
