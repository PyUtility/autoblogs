# -*- encoding: utf-8 -*-

import os
import streamlit as st

from dotenv import load_dotenv

from autoblogs.model.dataflows import AIModel, AIRequest
from autoblogs.manager.client import ClientManager
from autoblogs.manager.content import ContentManager
from autoblogs.error.error import AIClientError
from autoblogs.ui.components.render import render_page


def load_settings() -> dict:
    if "settings" not in st.session_state:
        load_dotenv()
        st.session_state["settings"] = dict(
            provider    = os.getenv("LLM_PROVIDER", "OPENAI"),
            modelname   = os.getenv("LLM_MODEL_NAME", ""),
            apikey      = os.getenv("LLM_MODEL_APIKEY", ""),
            base_url    = os.getenv("LLM_API_BASE_URL", ""),
            max_tokens  = int(os.getenv("MAX_TOKENS", "4096")),
            temperature = float(os.getenv("TEMPERATURE", "0.7")),
            outdir      = os.getenv("CONTENT_OUTPUT_DIR", "output"),
            context     = os.getenv("AGENT_PROMPT_CONTEXT", "base.txt.jinja"),
        )
    return st.session_state["settings"]


def create() -> None:
    st.title("📝 Create Content")
    st.divider()

    s = load_settings()

    with st.form("create_content", clear_on_submit = False):
        topic = st.text_input(
            "Content Topic",
            placeholder = "e.g. Linear Regression for Kids"
        )
        prompt = st.text_area(
            "Generation Prompt",
            placeholder = "Describe what the content should cover...",
            height = 120
        )
        keywords = st.text_input(
            "SEO Keywords (comma separated)",
            placeholder = "e.g. statistics, linear regression, machine learning"
        )
        submitted = st.form_submit_button("Generate Content", type = "primary")

    if submitted:
        if not topic.strip() or not prompt.strip():
            st.warning("Topic and Prompt are required.")
            return

        try:
            with st.spinner("Generating content..."):
                manager = ClientManager(
                    provider  = s["provider"],
                    modelname = s["modelname"],
                    apikey    = s["apikey"],
                    base_url  = s["base_url"] or None,
                )
                content = ContentManager(
                    outdir  = s["outdir"],
                    context = s["context"],
                )

                context = content.render(
                    topic          = topic,
                    tags           = keywords,
                    is_refinement  = False,
                    word_count_min = 800,
                    word_count_max = 1200,
                    n_sub_sections = 4,
                    using_claude   = manager.provider.name == "CLAUDE",
                )

                request = AIRequest(
                    topic   = topic,
                    prompt  = prompt,
                    context = context,
                )

                model = AIModel(
                    provider    = manager.provider,
                    useModel    = s["modelname"],
                    max_tokens  = s["max_tokens"],
                    temperature = s["temperature"],
                )

                response = manager.client(
                    model    = model,
                    request  = request,
                    apikey   = manager.apikey,
                    base_url = s["base_url"] or None,
                )

            st.session_state["response"] = response
            st.session_state["draft"]    = response.raw_response
            st.session_state["topic"]    = topic

            st.success("Content generated. Head to Draft Editor to review.")

            col1, col2, col3 = st.columns(3)
            col1.metric("Words",       response.word_count)
            col2.metric("Tokens Used", response.total_tokens)
            col3.metric("Latency (s)", f"{response.latency:.2f}")

        except AIClientError as e:
            st.error(f"Generation failed: {e}")


render_page(create)
