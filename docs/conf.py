# Configuration File for Sphinx Documentation Builder

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath(".."))

import autoblogs

# Project Information & Dynamic Version Configuration
project = "AutoBlogs"
copyright = "2025, Debmalya Pramanik (ZenithClowh)"
author = "Debmalya Pramanik (ZenithClown)"
release = autoblogs.__version__

# Extensions Configuration; Use MyST Parser (markdown) by Default
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary"
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".streamlit"]

# AutoDoc Configurations; https://stackoverflow.com/a/44638788/6623589
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": True
}

# Options for HTML Output; uses same source and build directories
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
