# -*- encoding: utf-8 -*-

"""
Auto Blogger - AI Requests / Response Data Models to Request Handles

Defines types :mod:`dataclasses` for all data flowing in and out of
the AI generation layer. Using :mod:`dataclasses` keeps the models
lightweight and framework-agnostic while still providing full type
hint coverage across any LLM agents.

These models are intentionally immutable (``frozen = True``). If a
response needs to be augmented, then create a new instance.
"""

import datetime as dt

from typing import Optional
from dataclasses import dataclass, field

@dataclass(frozen = True)
class AIModel:
    """
    Configuration of AI Model, Provider and Configuration

    The AI model configuration that globally defines the model to used,
    provider of the model and other general configuration settings.

    :type  model: str
    :param model: Name of the model, this can be any supported model
        that is widely available. The module accepts any types of
        models both open-source and/or proprietary models provided
        by different providers.

    :type  provider: str
    :param provider: Name of the provider, for example any open-source
        provider like ``ollama`` or proprietary models like ``claude``
        models. If a model requires an API key, then the same should
        be provided by the environment variables (for security).

    :type  max_tokens: int
    :param max_tokens: Maximum number of tokens the model can generate
        in its response. It does **not** limit the total tokens for
        the request - which is the total sum of input (prompt, system
        messages, retreived data) and output tokens (completion) and
        must stay within the model's context limit.

    :type  temperature: float
    :param temperature: A crucial settings in a large language models
        (LLMs) that controls the randomness and creativity of the
        model's output. A lower temperature makes the model more
        deterministic. Conversely, a higher temperature introduces
        more variability, but a very large value can produce less
        coherent outputs. Typically a value of ``0.70`` is generally
        considered as a good starting point.
    """

    model : str
    provider : str

    # general model configuration parameters, usage as per model
    max_tokens : int
    temperature : float


@dataclass(frozen = True)
class AIRequest:
    """
    Input Parameters for a Single AI Generation Output Call

    The request class handles a single generation call and provides
    handlers to format the response for any framework. The class
    carries everything a client needs to construct and send a prompt,
    including optional prior-draft context for refinement rounds.

    :type  topic: str
    :param topic: Topic name for the content/blog post/etc. which can
        typically be the redirect URL or page name.

    :type  prompt: str
    :param prompt: Detailed prompt required to generate the content,
        this can be a detailed string and related context can be
        added for finer controls.

    :type  context: str
    :param context: Context or additional data required to generate
        the content. This is optional, defaults to None.
    """

    topic : str
    prompt : str
    context : Optional[str] = None

    # request releated and content tagging/reviewer related details
    request_id : Optional[str] = None
    created_by : Optional[str] = None
    reviewed_by : Optional[str] = None

    created_at : dt.date = field(
        default_factory = lambda : dt.datetime.now().date()
    )
