# -*- encoding: utf-8 -*-

"""
Errors & Warnings Package for AutoBlogs
"""


from autoblogs.error.error import (
    AIClientError,
    AIRateLimitError,
    UndefinedModel
)

__all__ = [
    "AIClientError",
    "AIRateLimitError",
    "UndefinedModel"
]
