# -*- encoding: utf-8 -*-

"""
Custom Exception Definitions for AutoBlogs Module

All raised exceptions for :mod:`autoblogs` are documented here, such
that UI layer can properly handle any of the typed errors for an
efficient helpful message.
"""

class AIClientError(RuntimeError):
    """
    Raised when an AI API Calls Fails Unexpectedly

    Wraps HTTP errors, rate limit error, authentication failures, etc.
    formats for different providers and raises appropriate exceptions.
    """

    pass


class AIRateLimitError(AIClientError):
    """
    Sub-Class of :class:`AIRateLimitError` Raised on Rate Limitation

    A rate limit error typically occurs when the application exceeds
    the number of API requests within a specific amount of time. The
    class signals the ``@retry`` decorator that a ``back_off`` should
    be applied before the next attempt.
    """

    pass
