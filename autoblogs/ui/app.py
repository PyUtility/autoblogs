# -*- encoding: utf-8 -*-

"""
Streamlit UI Application Entry Point & Configuration

The launcher bootstraps the :mod:`streamlit` shell, initializes the
scheduler background engine, and wires the multi-page navigation for
:mod:`autoblogs` module. The file performs startup orchestration.
"""

import pathlib
import streamlit as st

from typing import Any, List

def build_pages(parent : pathlib.Path) -> List[Any]:
    """
    Build the Multi-Page Navigation for AutoBlogs UI

    The function returns a list of :class:`streamlit.Page` objects in
    the order of navigation menu. The function returns the underlying
    pages, title of the page and a custom icon.
    """

    path = parent / "pages"
    pages = [
        ("about.py", "About AutoBlogs UI", "📜"),
        ("dashboard.py", "Dashboard Page", "📊"),
        ("create.py", "Create Content", "🤖"),
        ("review.py", "Draft Editor", "✍"),
        ("settings.py", "Model Settings", "⚙")
    ]

    return [
        st.Page(path / page[0], title = page[1], icon = page[2])
        for page in pages
    ]


def load_style(parent : pathlib.Path) -> None:
    """
    Load the Style Sheet for AutoBlogs UI
    """

    path = parent / "assets/css/style.css"
    with open(path, "r", encoding = "utf-8") as f:
        style = f.read()

    st.markdown(f"<style>{style}</style>", unsafe_allow_html = True)
    return


if __name__ == "__main__":
    parent = pathlib.Path(__file__).parent # current directory

    st.set_page_config(
        page_title = "AutoBlogs UI", page_icon = "🔮",
        layout = "wide", initial_sidebar_state = "expanded"
    )

    load_style(parent = parent) # load style scheet; no error checks
    nav = st.navigation(build_pages(parent = parent))
    nav.run() # run the application; navigation engine
