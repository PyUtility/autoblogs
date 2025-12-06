# -*- encoding: utf-8 -*-

"""
AutoBlogs UI About Page - Understand the Application
"""

import streamlit as st

from autoblogs.ui.components.render import render_page # type: ignore

def dashboard() -> None:
    st.title("📜 About AutoBlogs UI")
    st.caption("Understand AutoBlogs UI")

    st.divider()

render_page(dashboard)
