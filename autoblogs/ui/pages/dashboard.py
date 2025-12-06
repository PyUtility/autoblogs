# -*- encoding: utf-8 -*-

"""
AutoBlogs UI Dashboard Page - Track Application State & Contents
"""

import streamlit as st

from autoblogs.ui.components.render import render_page # type: ignore

def dashboard() -> None:
    st.title("📊 Dashboard Page")
    st.caption("Track Application State & Contents")

    st.divider()

render_page(dashboard)
