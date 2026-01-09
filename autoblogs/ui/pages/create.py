# -*- encoding: utf-8 -*-

"""
AutoBlogs UI - Create a New Content
"""

import streamlit as st

from autoblogs.ui.components.render import render_page # type: ignore

def create() -> None:
    st.title("🤖 Create Content")
    st.divider()

    with st.form("create_content", clear_on_submit = True):
        title = st.text_input(
            label = "Topic Title",
            placeholder = "e.g. Linear Regreesion for Kids"
        )

        tags = st.text_input(
            label = "Content Tags (comma seperated)",
            placeholder = "e.g. statistics, linear regression"
        )

        submitted = st.form_submit_button(
            "Submit Topic", type = "primary"
        )

    # ? access to understand the user's requirement for content
    if submitted:
        tags = tags.strip().lower().split(",")
        st.markdown(f"## Title: {title}")

render_page(create)
