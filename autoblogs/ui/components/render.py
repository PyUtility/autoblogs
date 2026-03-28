# -*- encoding: utf-8 -*-

"""
Render Header & Footer Elements in Streamlit UI

Provides :func:`render_page`, a decorator-style helper that wraps any page
rendering function with a shared HTML header and footer, and injects the
footer-positioning script via :mod:`streamlit.components.v1` so it actually
executes in the browser.

:NOTE: ``st.markdown`` renders via React ``dangerouslySetInnerHTML`` which
       never executes ``<script>`` tags (browser innerHTML restriction).
       :func:`streamlit.components.v1.html` renders in a sandboxed iframe
       and uses ``window.parent`` to reach the main document.
"""

import pathlib
import streamlit as st
import streamlit.components.v1 as components

from typing import Callable


def render_page(function : Callable) -> None: # type: ignore
    """
    Wrap a Page Function with Shared Header and Footer

    Renders the HTML header, calls the page function, renders the HTML
    footer, then injects the footer-positioning JavaScript through a
    hidden ``components.html`` iframe so the script executes.

    :type  function: Callable
    :param function: Page rendering callable to wrap.

    :rtype:  None
    :return: None
    """
    parent = pathlib.Path(__file__).parent
    with open(parent / "header.html", "r", encoding = "utf-8") as f:
        header = f.read()
    with open(parent / "footer.html", "r", encoding = "utf-8") as f:
        footer = f.read()
    with open(parent / "footer.js", "r", encoding = "utf-8") as f:
        footer_js = f.read()

    st.markdown(header, unsafe_allow_html = True)
    function()
    st.markdown(footer, unsafe_allow_html = True)

    # ! script tags in st.markdown never execute; use components.html instead
    components.html(f"<script>{footer_js}</script>", height = 0)
    return
