# -*- encoding: utf-8 -*-

import streamlit as st

from autoblogs.config.default import homepage
from autoblogs.ui.components.render import render_page


def about() -> None:
    st.title("📜 About AutoBlogs UI")
    st.caption("AI-Assisted Human-Reviewed Content Generator")
    st.divider()

    st.markdown(f"""
AutoBlogs is an AI-powered content generation toolkit that supports multiple LLM providers
including **Claude (Anthropic)**, **OpenAI**, and **NVIDIA-NIM**.

**Workflow:**
1. Configure your LLM provider and API key in **Model Settings**
2. Enter a topic and prompt in **Create Content** to generate a blog post
3. Review, edit and save the draft in **Draft Editor**
4. Browse all saved content in **Dashboard**

**Supported Providers:** `CLAUDE` · `OPENAI` · `NVIDIA-NIM` · `LOCAL`

**Homepage:** [{homepage}]({homepage})
""")

    if "response" in st.session_state and st.session_state["response"]:
        r = st.session_state["response"]
        st.divider()
        st.subheader("Last Generation")
        col1, col2, col3 = st.columns(3)
        col1.metric("Words",        r.word_count)
        col2.metric("Total Tokens", r.total_tokens)
        col3.metric("Latency (s)",  f"{r.latency:.2f}")


render_page(about)
