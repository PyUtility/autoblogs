# -*- coding: utf-8 -*-

"""
AutoBlogs - AI-Powered Content Generation Toolkit
=================================================

An AI-assisted content generation tool that can leverage both open-source
and/or proprietary Large Language Model (LLM) agents to create
high-quality, SEO-optimized content for various needs. The system
integrates a *human-in-the-loop workflow*, ensuring that AI-generated
drafts can be reviewed, edited, and published.
"""

__version__ = "v0.0.1.dev0"

# ? added init time options registrations from aptracker/api.py
from autoblogs.api import * # noqa: F401, F403 # pyright: ignore[reportMissingImports]
