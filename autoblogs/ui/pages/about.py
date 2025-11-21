import streamlit as st

from autoblogs.ui.components.render import render_page # type: ignore

def about() -> None:
    st.title("My Streamlit App - BAOUT Page")
    st.write("Launched via pyproject.toml entry point!")

render_page(about)
