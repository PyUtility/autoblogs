# -*- encoding: utf-8 -*-

"""
Provide a Unified Abstract AI Client for AutoBlogs Module

Provides an abstract ``AIClient`` base class that can be inherited by
the concrete classes for different different providers. The clients
are defined in a generic way and provides base abstract method that
has to be implemented in the concrete classes.
"""

import abc

from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse

class AIClient(abc.ABC):
    """
    Abstract AI Client Interface for Content Generation

    The abstract class provides a built-in default class ``generate``
    that can be used uniformly across any concrete models. The
    abstract methods provide default signature which is enforced to
    remain the same in the concrete classes.
    """

    def __init__(self, model : AIModel) -> None:
        self.model = model.model # directly use data class attributes


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
