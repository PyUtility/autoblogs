# -*- encoding: utf-8 -*-

import os
import pathlib
import streamlit as st

from dotenv import load_dotenv

from autoblogs.ui.components.render import render_page


def dashboard() -> None:
    st.title("📊 Dashboard")
    st.caption("Track Application State & Contents")
    st.divider()

    s = st.session_state.get("settings", {})
    if not s:
        load_dotenv()

    outdir = s.get("outdir", os.getenv("CONTENT_OUTPUT_DIR", "output"))

    if not outdir or not pathlib.Path(outdir).exists():
        st.warning(f"Output directory `{outdir}` does not exist.")
        return

    files = sorted(
        [f for f in pathlib.Path(outdir).glob("*") if f.is_file()],
        key     = lambda f : f.stat().st_mtime,
        reverse = True
    )

    if not files:
        st.info("No files found in the output directory.")
        return

    st.metric("Total Files", len(files))
    st.divider()

    for f in files:
        size_kb = f.stat().st_size / 1024

        with st.expander(f.name):
            col1, col2 = st.columns([3, 1])
            col1.caption(f"Path: `{f}`")
            col2.caption(f"Size: `{size_kb:.1f} KB`")

            if f.suffix in (".md", ".txt"):
                with open(f, "r", encoding = "utf-8") as fp:
                    st.code(fp.read()[:2000], language = "markdown")


render_page(dashboard)
