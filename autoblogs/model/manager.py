# -*- encoding: utf-8 -*-

"""
Typical Orchestration of Content using Persistent Manager

Orchestrates the full blog-post lifecycle from Topic creation through
AI generation, draft refinement, human approval, and final publishing.
"""

import pathlib

from autoblogs.client.base import AIClient

class ContentManager:
    """
    Content Life Cycle Manager for an LLM Agentic Model

    Manages topics drafts and final content before publishing. The
    manager also controls the session state in the Streamlit UI.

    :type  client: AIClient
    :param client: Currently active LLM Agent Client that can generate
        content. This should be one of the derived concrete class.

    :type  outdir: pathlib.Path
    :param outdir: Output directory to store the generated content,
        should be a valid directory.

    :type  verbose: bool
    :param verbose: Enable verbose print output, defaults to ``False``
        for console and/or terminal logging/
    """

    def __init__(
        self,
        client : AIClient,
        outdir : pathlib.Path,
        verbose : bool = False
    ) -> None:
        """
        Initialization of Content Manager Object
        """

        self.client = client
        self.outdir = outdir
        self.verbose = verbose
