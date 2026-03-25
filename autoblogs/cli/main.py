# -*- encoding: utf-8 -*-

"""
CLI Application for AutoBlogs - Content Creation Tool
"""

import os
import getpass
import pathlib

from dotenv import load_dotenv

from autoblogs.prompts import PROMPT_BLOGS
from autoblogs.client.claude import ClaudeClient
from autoblogs.client.openai import OpenAIClient
from autoblogs.config.constants import AIProvider
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse

def config(username : str, homepage : str) -> None:
    root = pathlib.Path(__file__).parent / "static"
    art = open(root / "ascii.graffiti.txt", "r").read()

    print(f"\033[96m{art}\033[0m", end = "\n\n")
    print(
        f"Welcome \033[1m{username}\033[0m to AutoBlogs CLI! "
        "Please enter the following information (or select defaults)."
        f"\n\033[1m\033[92m  >> Homepage: {homepage}\033[0m\n\n"
    )

    global topic, prompt, aiclient, apikey, baseuri

    providers = " | ".join([
        provider.name for provider in AIProvider # type: ignore
    ])
    print(f"Available AI Provider  : {providers}")
    provider =input("Select the AI Provider : ")

    aiclient = {
        "CLAUDE" : ClaudeClient
    }.get(provider, OpenAIClient)

    print("\n\nSet the API Key in Environment Variable\n")

    topic  = input("Topic of the Blog      : ")
    prompt = input("Elaborate Requirements : ")

    load_dotenv()
    apikey = os.getenv("LLM_MODEL_APIKEY")
    baseuri = os.getenv("LLM_API_BASE_URL") \
        if provider == "NVIDIA-NIM" else None
    return


def launch() -> AIResponse:
    config(
        username = getpass.getuser(),
        homepage = "https://github.com/PyUtility/autoblogs"
    )

    model = AIModel(
        model = "nvidia/nemotron-content-safety-reasoning-4b"
    )
    request = AIRequest(
        topic = topic, prompt = prompt, context = PROMPT_BLOGS
    )

    client = aiclient(
        model = model, apikey = apikey, base_url = baseuri # type: ignore
    )

    response = client.generate(request = request)
    print(response.raw_response)

    return response

if __name__ == "__main__":
    launch()
