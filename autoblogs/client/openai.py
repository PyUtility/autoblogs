# -*- encoding: utf-8 -*-

"""
Set the OpenAI Client SDK Interface for Supported Channels
"""


import time
import openai

from typing import Optional
from uuid import uuid4 as UUIDx

from autoblogs.error import AIClientError, AIRateLimitError
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse

def generateOpenAI(
        model : AIModel, request : AIRequest,
        apikey : str, base_url : Optional[str] = None
    ) -> AIResponse:
    """
    Open AI API Client for Content Generation

    Wraps the ``openai`` SDK's messages API using the ``model.*``
    to generate content. The model is the concrete implementation of
    the :class:`AIClient` for Open AI SDK. On using this model,
    :mod:`openai` is required, which is imported at initialization.

    The class can also be used for `NVDIA-NIM` AI Agents, by using
    endpoints from (``https://integrate.api.nvidia.com/v1``) which
    exposes OpenAI compatible completion interfaces.
    """

    start = time.monotonic()
    client = openai.OpenAI(
            api_key = apikey, base_url = base_url
        )

    # Context holds the required Jinja2 Template
    # The Context can only be send as ``messages`` argument
    messages = [{"role" : "system", "content" : request.prompt}]

    if request.context:
        messages.append({
            "role" : "system", "content" : request.context
        })

    try:
        response = client.chat.completions.create(
            model = model.useModel, # type: ignore
            max_tokens = model.max_tokens,
            temperature = model.temperature,

            # messages is the actual content block, user role
            messages = messages # type: ignore
        )
    except openai.RateLimitError as e:
        raise AIRateLimitError(f"Rate Limit Reached: {e}") from e
    except openai.APIError as e:
        raise AIClientError(f"Claude API Error: {e}") from e

    raw_response = response.choices[0].message.content \
        if response.choices else None # failed to get any response

    # Generate AIResponse() Method and Return
    return AIResponse(
        request_id = request.request_id or str(UUIDx()),
        raw_response = raw_response,
        in_tokens = response.usage.prompt_tokens, # type: ignore
        out_tokens = response.usage.completion_tokens, # type: ignore
        latency = time.monotonic() - start
    )
