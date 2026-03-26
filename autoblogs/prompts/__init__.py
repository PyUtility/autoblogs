# -*- encoding: utf-8 -*-

"""
Read & Format the Prompt as per the Front Matter with Parameter Control

Using the :mod:`jinja2` templating engine, the following context are
loaded to create better content. Check the individual prompt template
file on the variable to understand the context.
"""

import jinja2
import pathlib

PROMPT_DIRECTORY = pathlib.Path(__file__).parent

def render(filename : str, **kwargs) -> str:
    env = jinja2.Environment(
        loader = jinja2.FileSystemLoader(str(PROMPT_DIRECTORY))
    )
    return env.get_template(filename).render(**kwargs).strip()
