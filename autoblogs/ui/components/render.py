# -*- encoding: utf-8 -*-

"""
Render Header & Footer Elements in Streamlit UI
"""

import pathlib
import streamlit as st

from typing import Callable

def render_page(function : Callable) -> None: # type: ignore
    parent = pathlib.Path(__file__).parent
    with open(parent / "header.html", "r", encoding = "utf-8") as f:
        header = f.read()
    with open(parent / "footer.html", "r", encoding = "utf-8") as f:
        footer = f.read()

    st.markdown(header, unsafe_allow_html = True)
    function()
    st.markdown(footer, unsafe_allow_html = True)
    return
