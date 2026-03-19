# -*- encoding: utf-8 -*-

"""
Read the Example Prompt and Return as a Python Variable
"""

from importlib import resources

with resources.files(__package__).joinpath("prompts/blogs.txt").open("r", encoding = "utf-8") as f:
    PROMPT_BLOGS = f.read()
