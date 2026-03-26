# -*- encoding: utf-8 -*-

"""
Provide a Unified Abstract AI Client for AutoBlogs Module

Provides an abstract ``AIClient`` base class that can be inherited by
the concrete classes for different different providers. The clients
are defined in a generic way and provides base abstract method that
has to be implemented in the concrete classes.
"""

import abc

from typing import Optional

from autoblogs.config.constants import (
    AIProvider, ClaudeModel, OpenAIModel
)
from autoblogs.error import UndefinedModel
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
