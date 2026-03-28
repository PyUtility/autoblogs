# -*- encoding: utf-8 -*-

"""
Typical Orchestration of Content using a Persistent Manager

Orchestrates the full blog-post lifecycle from Topic creation through
AI generation, draft refinement, human approval, and final publishing.
The content manager also controls the different types of content that
may be required to fine tune the final output.
"""

import jinja2
import pathlib

from typing import Callable

from autoblogs.directory import promptsdir

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

    :type  context: str
    :param context: The context sets the LLM Agent's memory and is
        required to generate the content in a better manner. A set of
        default context templates are provided in the module directory
        (``autobogs/prompts``) which uses the :mod:`jinja2` template.

    :type  verbose: bool
    :param verbose: Enable verbose print output, defaults to ``False``
        for console and/or terminal logging/
    """

    def __init__(
        self,
        client : Callable,
        outdir : pathlib.Path,
        context : str = "base.txt.jinja",
        verbose : bool = False
    ) -> None:
        """
        Initialization of Content Manager Object
        """

        self.client = client
        self.outdir = outdir
        self.context = context
        self.verbose = verbose


    def render(self, **kwargs) -> str:
        """
        Read & Format the Prompt as per the Front Matter Control

        Using the :mod:`jinja2` templating engine, the following
        context are loaded to create better content. Check the
        individual prompt template file on the variable to understand,
        or generate one as per requirement.
        """

        env = jinja2.Environment(
            loader = jinja2.FileSystemLoader(str(promptsdir))
        )
        return env.get_template(self.context).render(**kwargs).strip()


    def writefile(self, content : str, filename : str) -> None:
        pass
