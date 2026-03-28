# -*- encoding: utf-8 -*-

"""
Set the Anthopic Client SDK Interface for Supported Channels
"""

import time
import anthropic

from uuid import uuid4 as UUIDx

from autoblogs.error.error import AIClientError, AIRateLimitError
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse


def claudeGenerate(
        model : AIModel, request : AIRequest, apikey : str, **_
    ) -> AIResponse:
    """
    Anthropic Claude API Client to Generate Content(s) from Prompt

    Wraps the ``anthropic`` SDK's messages API using the ``model.*``
    to generate content. The model is the concrete implementation of
    the :class:`AIClient` for Anthropic SDK. On using this model,
    :mod:`anthropic` is required, which is imported at initialization.

    Generate the response (content) based on the request (prompt) from
    the LLM agents. The concrete function should be able to model the
    data in the form of :class:`AIResponse` type.

    :type  model: AIModel
    :param model: Name of the model that the provider supports, or if
        any alue is permitted then pass the same value.

    :type  request: AIRequest
    :param request: Fully-constructed request to generate the prompt,
        including prompt and context.

    **Return Values**

    Model the response of the LLM agent in the following format that
    may also include dynamic informaiton.

    :rtype:  AIResponse
    :return: AI response with additional information like author,
        reviewer, etc. Check data class for more information.
    """

    start = time.monotonic()
    client = anthropic.Anthropic(api_key = apikey)

    # Context holds the required Jinja2 Template
    # The Context should be sent as ``system`` Argument
    config : dict = dict(
        model = model.useModel,
        max_tokens = model.max_tokens,
        temperature = model.temperature,

        # messages is the actual content block, user role
        messages = [{
            "role" : "user", "content" : request.prompt
        }]
    )

    if request.context:
        config["system"] = request.context

    try:
        response = client.messages.create(**config)
    except anthropic.RateLimitError as e:
        raise AIRateLimitError(f"Rate Limit Reached: {e}") from e
    except anthropic.APIError as e:
        raise AIClientError(f"Claude API Error: {e}") from e

    raw_response = response.content[0].text if response.content \
        else None # failed to get any response

    # Generate AIResponse() Method and Return
    return AIResponse(
        request_id = request.request_id or str(UUIDx()),
        raw_response = raw_response,
        in_tokens = response.usage.input_tokens,
        out_tokens = response.usage.output_tokens,
        latency = time.monotonic() - start
    )


