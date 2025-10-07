# -*- encoding: utf-8 -*-

"""
Provide Concrete Ancthopic Claude AI Client
"""

from autoblogs.client._base import AIClient
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse

class ClaudeClient(AIClient):
    """
    Anthropic Claude API Client to Generate Content

    Wraps the ``anthropic`` SDK's messages API using the ``model.*``
    to generate content. Since the client honours the ``@retry``
    decorator from the :mod:`autoblogs.utils.retry` we can re-attempt
    without closing the existing connection. Rate-limit responses are
    re-raised as :class:`~app.src.errors.errors.AIRateLimitError` so
    the ``@retry`` decorator can handle them transparently.
    """

    def __init__(
        self,
        model : AIModel,
        apikey : str | None = None
    ) -> None:
        super().__init__(model = model, apikey = apikey)


    @retry(
        max_attempts = 3,
        backoff_factor = 2.0,
        retry_on = AIRateLimitError
    )
    def generate(self, request : AIRequest) -> AIResponse:
        pass
