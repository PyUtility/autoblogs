# -*- encoding: utf-8 -*-

"""
CLI Application for AutoBlogs - Content Creation Tool

Entry point for the command-line interface. Displays the ASCII art
banner, collects the blog topic and additional requirements from the
user, renders the structured Jinja2 prompt template, and invokes the
appropriate LLM client to generate a blog post.

:NOTE: Requires ``LLM_MODEL_APIKEY`` (and ``LLM_API_BASE_URL`` for the
    ``NVIDIA-NIM`` provider) to be set in the environment or a ``.env``
    file before running.
"""

import os
import getpass
import pathlib

from dotenv import load_dotenv

from autoblogs.config.default import homepage
from autoblogs.model.dataflows import AIModel
from autoblogs.manager.client import ClientManager
from autoblogs.manager.content import ContentManager
from autoblogs.model.dataflows import AIRequest, AIResponse

def welcome() -> None:
    """
    CLI Welcome Message - Greet User & Print the Banner
    """

    asciiart = pathlib.Path(__file__).parent / "static"
    asciiart = open(asciiart / "ascii.graffiti.txt", "r").read()

    print(f"\033[96m{asciiart}\033[0m", end = "\n\n")
    print(
        f"Welcome \033[1m{getpass.getuser()}\033[0m to AutoBlogs CLI! "
        "Please enter the following information (or select defaults)."
        f"\n\033[1m\033[92m  >> Homepage: {homepage}\033[0m\n\n"
    )

    return


def launch() -> AIResponse:
    """
    Launch the AutoBlogs CLI Content Generation Workflow

    Orchestrates the full generation pipeline: displays the welcome
    banner, prompts the user for the blog topic and requirements,
    renders the Jinja2 prompt template, instantiates the LLM client
    via :func:`getClient`, and prints the generated post.

    :rtype:  AIResponse
    :return: Complete AI response including the raw Markdown blog post
        and token-usage metrics.
    """

    welcome()
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER")
    modelname = os.getenv("LLM_MODEL_NAME")
    apikey  = os.getenv("LLM_MODEL_APIKEY")
    base_url = os.getenv("LLM_API_BASE_URL")

    max_tokens = os.getenv("MAX_TOKENS")
    temperature = os.getenv("TEMPERATURE")

    # get the client and content manager, and initialize
    client = ClientManager(
        provider = provider, modelname = modelname, # type: ignore
        apikey = apikey, base_url = base_url
    )
    content = ContentManager(outdir = None) # TODO # type: ignore

    # the final resolved client function, return after checks
    method = client.client

    # additional inputs for the render engine
    topic    = input("\nSet the Content Topic (one-line): ")
    prompt   = input("Explain the Prompt to Generate Content: ")
    keywords = input("Set SEO Keywords (comma seperated): ")

    # ! render the Jinja2 template before building the request — both clients
    # ! only forward request.prompt to the API; request.context is not sent
    context = content.render(
        topic = topic, tags = keywords,
        is_refinement = False, word_count_min = 800,
        word_count_max = 1200, n_sub_sections = 4,
        using_claude = client.provider.name == "CLAUDE",
    )

    request = AIRequest(
        topic   = topic,
        prompt  = prompt,
        context = context,
    )

    model = AIModel(
        provider = client.provider,
        useModel = os.getenv("LLM_MODEL_NAME"),
        max_tokens = max_tokens, # type: ignore
        temperature = temperature # type: ignore
    )

    response = method(
        model = model,
        request = request,
        apikey = client.apikey, # type: ignore
        base_url = base_url
    )

    return response
