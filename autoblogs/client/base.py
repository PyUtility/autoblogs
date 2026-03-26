# -*- encoding: utf-8 -*-

"""
Provide a Unified Abstract AI Client for AutoBlogs Module

Provides an abstract ``AIClient`` base class that can be inherited by
the concrete classes for different different providers. The clients
are defined in a generic way and provides base abstract method that
has to be implemented in the concrete classes.
"""

import abc
import time

from typing import Optional
from uuid import uuid4 as UUIDx

from autoblogs.config.constants import (
    AIProvider, ClaudeModel, OpenAIModel
)
from autoblogs.error import UndefinedModel
from autoblogs.error import AIClientError, AIRateLimitError
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse

class AIClient(abc.ABC):
    """
    Abstract AI Client Interface for Content Generation

    The abstract class provides a built-in default class ``generate``
    that can be used uniformly across any concrete models. The
    abstract methods provide default signature which is enforced to
    remain the same in the concrete classes.
    """

    def __init__(self, apikey : Optional[str]) -> None:
        self.model = self.__set_model__()
        self.apikey = apikey # any valid key, or none if not required


    def __set_model__(self) -> AIModel:
        provider = [ (elem.value, elem.name) for elem in AIProvider ]
        provider = input(
            "Select an AI Provider\n"
            + "\n".join([f"  >> {x[0]:<2} : {x[1]}" for x in provider])
            + "\n User Choice [LOCAL]: "
        ) or "LOCAL"

        try:
            provider = AIProvider(provider.upper()) \
                if provider.upper() in AIProvider.__members__ \
                else AIProvider(int(provider))
        except (KeyError, ValueError):
            raise UndefinedModel(model = provider)

        # ? Select the Model based on the AI Provider / ANY
        models = dict(CLAUDE = ClaudeModel, OPENAI = OpenAIModel)
        models = models.get(provider.name, None)

        if models:
            options = [ (elem.value, elem.name) for elem in models ]
            model = input(
                "Select an AI Model\n"
                + "\n".join([f"  >> {x[0]:<2} : {x[1]}" for x in options])
                + "\n User Choice: "
            )

            try:
                model = models[model.upper()] \
                    if model.upper() in models.__members__ \
                    else models(int(model))
            except (KeyError, ValueError):
                model = model.upper()

        # ? Select other model options, or use defaults:
        max_tokens = int(input("Max. Tokens [4096]: ")) or 4096
        temperature = float(input("Temperature [0.7]: ")) or 0.7

        return AIModel(
            provider = provider,
            useModel = model, # type: ignore
            max_tokens = max_tokens,
            temperature = temperature
        )


    @abc.abstractmethod
    def generate(self, request : AIRequest) -> AIResponse:
        """
        Unified Method to Generate AI Response for a Given Request

        Generate the response (content) based on the request (prompt)
        from the LLM agents. The concrete function should be able to
        model the data in the form of :class:`AIResponse` type.

        :type  request: AIRequest
        :param request: Fully-constructed request to generate the
            prompt, including prompt and context.

        **Return Values**

        Model the response of the LLM agent in the following format
        that may also include dynamic informaiton.

        :rtype:  AIResponse
        :return: AI response with additional information like author,
            reviewer, etc. Check data class for more information.
        """

        pass


class ClaudeClient(AIClient):
    """
    Anthropic Claude API Client to Generate Content(s) from Prompt

    Wraps the ``anthropic`` SDK's messages API using the ``model.*``
    to generate content. The model is the concrete implementation of
    the :class:`AIClient` for Anthropic SDK. On using this model,
    :mod:`anthropic` is required, which is imported at initialization.
    """

    def __init__(self, apikey : str) -> None:
        import anthropic
        super().__init__(apikey = apikey)

        # create the client object; this is different for each model
        self.client = anthropic.Anthropic(api_key = self.apikey)


    def generate(self, request : AIRequest) -> AIResponse:
        """
        Generate Content via the Antrhopic Messages API
        """

        start = time.monotonic()

        # Context holds the required Jinja2 Template
        # The Context should be sent as ``system`` Argument
        config : dict = dict(
            model = self.model.useModel,
            max_tokens = self.model.max_tokens,
            temperature = self.model.temperature,

            # messages is the actual content block, user role
            messages = [{
                "role" : "user", "content" : request.prompt
            }]
        )

        if request.context:
            config["system"] = request.context

        try:
            response = self.client.messages.create(**config)
        except anthropic.RateLimitError as e: # type: ignore
            raise AIRateLimitError(f"Rate Limit Reached: {e}") from e
        except anthropic.APIError as e: # type: ignore
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


class OpenAIClient(AIClient):
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

    def __init__(
            self, apikey : str, base_url : Optional[str] = None
    ) -> None:
        import openai
        super().__init__(apikey = apikey)

        # create the client object; this is different for each model
        self.client = openai.OpenAI(
            api_key = self.apikey, base_url = base_url
        )


    def generate(self, request : AIRequest) -> AIResponse:
        """
        Generate Content via the Antrhopic Messages API
        """

        start = time.monotonic()

        # Context holds the required Jinja2 Template
        # The Context can only be send as ``messages`` argument
        messages = [{"role" : "system", "content" : request.prompt}]

        if request.context:
            messages.append({
                "role" : "system", "content" : request.context
            })

        try:
            response = self.client.chat.completions.create(
                model = self.model.useModel, # type: ignore
                max_tokens = self.model.max_tokens,
                temperature = self.model.temperature,

                # messages is the actual content block, user role
                messages = messages # type: ignore
            )
        except openai.RateLimitError as e: # type: ignore
            raise AIRateLimitError(f"Rate Limit Reached: {e}") from e
        except openai.APIError as e: # type: ignore
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
