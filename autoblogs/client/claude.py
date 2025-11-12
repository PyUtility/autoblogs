# -*- encoding: utf-8 -*-

"""
Provide Concrete Ancthopic Claude AI Client
"""

import time
import uuid
import anthropic

from autoblogs.client._base import AIClient
from autoblogs.error import AIClientError, AIRateLimitError
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
        self.client = anthropic.Anthropic(api_key = self.apikey)


    def generate(self, request : AIRequest) -> AIResponse:
        """
        Generate Content via the Antrhopic Messages API
        """

        start = time.monotonic()

        try:
            response = self.client.messages.create(
                model = self.model.model,
                max_tokens = self.model.max_tokens,
                temperature = self.model.temperature,
                messages = [{
                    "role" : "user", "content" : request.prompt
                }]
            )
        except anthropic.RateLimitError as e:
            raise AIRateLimitError(f"Rate Limit Reached: {e}") from e
        except anthropic.APIError as e:
            raise AIClientError(f"Claude API Error: {e}") from e

        latency = time.monotonic() - start
        raw_response = response.content[0].text if response.content \
            else None # failed to get any response
        
        print(
            f"VERBOSE: ClaudeClient.generate({request.topic[:40]}...)"
        )

        return AIResponse(
            request_id = request.request_id or str(uuid.uuid4()),
            raw_response = raw_response,
            in_tokens = response.usage.input_tokens,
            out_tokens = response.usage.output_tokens,
            latency = latency
        )
