# -*- encoding: utf-8 -*-

"""
Define the Module Level Default Value(s) for AutoBlogs
"""

from autoblogs.config.constants import AIProvider

homepage = "https://github.com/PyUtility/autoblogs"
newissue = f"{homepage}/issues/new/choose"

defaultmodel = AIProvider.LOCAL

__all__ = ["homepage", "newissue", "defaultmodel"]
