# -*- encoding: utf-8 -*-

"""
Provide a Unified Abstract AI Client for AutoBlogs Module

Provides an abstract ``AIClient`` base class that can be inherited by
the concrete classes for different different providers. The clients
are defined in a generic way and provides base abstract method that
has to be implemented in the concrete classes.
"""

import time

from uuid import uuid4 as UUIDx
from typing import Callable, Optional, Union

from autoblogs.config.constants import (
    AIProvider, ClaudeModel, OpenAIModel
)
from autoblogs.error import UndefinedModel
from autoblogs.config.constants import AIProvider
from autoblogs.error import AIClientError, AIRateLimitError
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse

class AIClient(object):
    """
    Abstract AI Client Interface for Content Generation

    The abstract class provides a built-in default class ``generate``
    that can be used uniformly across any concrete models. The
    abstract methods provide default signature which is enforced to
    remain the same in the concrete classes.
    """

    def __init__(self, apikey : Optional[str]) -> None:
        self.apikey = apikey # any valid key, or none if not required

        # Set AI Provider based on User Input/UI Calls (TODO)
        self.provider = self.__set_provider__()

        # Set the Model Name based on the Provider Name
        self.model = self.__set_model__(provider = self.provider)

        # Set other Model Controls (TODO Method) for Inputs
        self.max_tokens = int(input("Max. Tokens [4096]: ") or 4096)
        self.temperature = float(input("Temperature [0.7]: ") or 0.7)


    @property
    def AIModel(self) -> AIModel:
        return AIModel(
            provider = self.provider,
            useModel = self.model, # type: ignore
            max_tokens = self.max_tokens,
            temperature = self.temperature
        )


    def __set_provider__(self) -> AIProvider:
        provider = [ (elem.value, elem.name) for elem in AIProvider ]
        selection = input(
            "Select an AI Provider\n"
            + "\n".join([f"  >> {x[0]:<2} : {x[1]}" for x in provider])
            + "\n User Choice [LOCAL]: "
        ) or "LOCAL"

        try:
            provider = AIProvider[selection.upper()] \
                if selection.upper() in AIProvider.__members__ \
                else AIProvider(int(selection))
        except (KeyError, ValueError):
            raise UndefinedModel(model = selection)
        
        return provider


    def __set_model__(
            self, provider : AIProvider
    ) -> Union[ClaudeModel, OpenAIModel, str]:
        models = dict(CLAUDE = ClaudeModel, OPENAI = OpenAIModel)
        models = models.get(provider.name, None)

        model = None
        if models:
            options = [ (elem.value, elem.name) for elem in models ]
            selection = input(
                "Select an AI Model\n"
                + "\n".join([f"  >> {x[0]:<2} : {x[1]}" for x in options])
                + "\n User Choice: "
            )

            try:
                model = models[selection.upper()] \
                    if selection.upper() in models.__members__ \
                    else models(int(selection))
            except (KeyError, ValueError):
                model = selection.upper()
        else:
            model = "https://localhost:11434"

        return model


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

    import anthropic
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

    import openai
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
