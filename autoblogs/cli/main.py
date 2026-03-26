# -*- encoding: utf-8 -*-

"""
CLI Application for AutoBlogs - Content Creation Tool

Entry point for the command-line interface. Collects user input (provider,
topic, and additional requirements), renders the structured Jinja2 prompt
template with the chosen topic and default word-count bounds, and invokes
the appropriate LLM client to generate a blog post.

:NOTE: Requires ``LLM_MODEL_APIKEY`` (and ``LLM_API_BASE_URL`` for the
    ``NVIDIA-NIM`` provider) to be set in the environment or a ``.env``
    file before running.
"""

import os
import getpass
import pathlib

from dotenv import load_dotenv

from autoblogs.prompts import render
from autoblogs.client.claude import ClaudeClient
from autoblogs.client.openai import OpenAIClient
from autoblogs.config.constants import AIProvider
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse


# ! update these when newer model versions are released
_DEFAULT_MODELS : dict[str, str] = {
    "CLAUDE"     : "claude-opus-4-6",
    "OPENAI"     : "gpt-4o",
    "NVIDIA-NIM" : "nvidia/nemotron-content-safety-reasoning-4b",
}

_DEFAULT_MODEL_FALLBACK : str = "gpt-4o"


def config(username : str, homepage : str) -> None:
    """
    Configure CLI Session Parameters via Interactive Input

    Displays the ASCII banner, prompts the user to select an AI provider,
    enter the blog topic and additional requirements, and loads the API
    credentials from the environment or ``.env`` file.

    :type  username: str
    :param username: OS username shown in the welcome banner.

    :type  homepage: str
    :param homepage: Project homepage URL shown in the welcome banner.
    """

    root = pathlib.Path(__file__).parent / "static"
    art  = open(root / "ascii.graffiti.txt", "r").read()

    print(f"\033[96m{art}\033[0m", end = "\n\n")
    print(
        f"Welcome \033[1m{username}\033[0m to AutoBlogs CLI! "
        "Please enter the following information (or select defaults)."
        f"\n\033[1m\033[92m  >> Homepage: {homepage}\033[0m\n\n"
    )

    global topic, prompt, provider, aiclient, apikey, baseuri

    available = " | ".join([
        p.name for p in AIProvider  # type: ignore
    ])
    print(f"Available AI Provider  : {available}")
    provider = input("Select the AI Provider : ")

    aiclient = {
        "CLAUDE" : ClaudeClient
    }.get(provider, OpenAIClient)

    print("\n\nSet the API Key in Environment Variable\n")

    topic  = input("Topic of the Blog      : ")
    prompt = input("Elaborate Requirements : ")

    load_dotenv()
    apikey  = os.getenv("LLM_MODEL_APIKEY")
    baseuri = os.getenv("LLM_API_BASE_URL") \
        if provider == "NVIDIA-NIM" else None


def launch() -> AIResponse:
    """
    Launch the AutoBlogs CLI Content Generation Workflow

    Orchestrates the full generation pipeline: collects user input via
    :func:`config`, renders the Jinja2 prompt template with the chosen
    topic and sensible defaults, selects the correct model name for the
    provider, instantiates the LLM client, and prints the generated post.

    :rtype:  AIResponse
    :return: Complete AI response including the raw Markdown blog post and
        token-usage metrics.
    """

    config(
        username = getpass.getuser(),
        homepage = "https://github.com/PyUtility/autoblogs"
    )

    # ! render the Jinja2 template before building the request — both clients
    # ! only forward request.prompt to the API; request.context is not sent
    context = render(
        filename        = "python.txt.jinja",
        topic           = topic,
        tags            = [],
        is_refinement   = False,
        word_count_min  = 800,
        word_count_max  = 1200,
        n_sub_sections  = 4,
        using_claude    = provider == "CLAUDE",
    )

    model_name = _DEFAULT_MODELS.get(provider, _DEFAULT_MODEL_FALLBACK)
    model      = AIModel(model = model_name)

    request = AIRequest(
        topic   = topic,
        prompt  = prompt,
        context = context,
    )

    # ? base_url applies only to NVIDIA-NIM which uses a custom OpenAI-compatible endpoint
    if provider == "NVIDIA-NIM":
        client = aiclient(
            model = model, apikey = apikey, base_url = baseuri  # type: ignore[call-arg]
        )
    else:
        client = aiclient(  # type: ignore
            model = model, apikey = apikey
        )

    response = client.generate(request = request)
    print(response.raw_response)

    return response


if __name__ == "__main__":
    launch()
