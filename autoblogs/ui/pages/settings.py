# -*- encoding: utf-8 -*-

import os
import streamlit as st

from dotenv import load_dotenv

from autoblogs.ui.components.render import render_page


def settings() -> None:
    st.title("⚙ Model Settings")
    st.divider()

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

    s         = st.session_state["settings"]
    providers = ["CLAUDE", "OPENAI", "NVIDIA-NIM", "LOCAL"]
    templates = ["base.txt.jinja", "python.txt.jinja"]

    with st.form("model_settings"):
        st.subheader("LLM Provider")

        provider = st.selectbox(
            "Provider", options = providers,
            index = providers.index(s["provider"]) if s["provider"] in providers else 1
        )

        col1, col2 = st.columns(2)
        with col1:
            modelname = st.text_input("Model Name", value = s["modelname"])
        with col2:
            apikey = st.text_input("API Key", value = s["apikey"], type = "password")

        base_url = st.text_input(
            "Base URL (required for NVIDIA-NIM / LOCAL)", value = s["base_url"]
        )

        st.subheader("Generation Parameters")

        col3, col4 = st.columns(2)
        with col3:
            max_tokens = st.number_input(
                "Max Tokens", min_value = 256, max_value = 32768,
                value = int(s["max_tokens"])
            )
        with col4:
            temperature = st.slider(
                "Temperature", min_value = 0.0, max_value = 2.0,
                value = float(s["temperature"]), step = 0.1
            )

        st.subheader("Content Settings")

        col5, col6 = st.columns(2)
        with col5:
            outdir = st.text_input("Output Directory", value = s["outdir"])
        with col6:
            context = st.selectbox(
                "Prompt Template", options = templates,
                index = templates.index(s["context"]) if s["context"] in templates else 0
            )

        saved = st.form_submit_button("Save Settings", type = "primary")

    if saved:
        st.session_state["settings"] = dict(
            provider    = provider,
            modelname   = modelname,
            apikey      = apikey,
            base_url    = base_url,
            max_tokens  = int(max_tokens),
            temperature = float(temperature),
            outdir      = outdir,
            context     = context,
        )
        st.success("Settings saved.")


render_page(settings)
