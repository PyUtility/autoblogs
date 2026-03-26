# -*- encoding: utf-8 -*-

"""
Provide Concrete Class for Open AI & NVIDIA-NIM Client
"""

import time
import uuid

from autoblogs.client.base import AIClient
from autoblogs.error import AIClientError, AIRateLimitError
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse

class OpenAIClient(AIClient):
    """
    Open AI API Client for Content Generation

    Wraps the ``openai`` SDK's messages API using the ``model.*``
    to generate content. Since the client honours the ``@retry``
    decorator from the :mod:`autoblogs.utils.retry` we can re-attempt
    without closing the existing connection. Rate-limit responses are
    re-raised as :class:`~app.src.errors.errors.AIRateLimitError` so
    the ``@retry`` decorator can handle them transparently.

    The class can also be used for `NVDIA-NIM` AI Agents, by using
    endpoints from (``https://integrate.api.nvidia.com/v1``) which
    exposes OpenAI compatible completion interfaces.
    """

    def __init__(
        self,
        model : AIModel,
        apikey : str | None = None,
        base_url : str | None = None
    ) -> None:
        import openai

        super().__init__(model = model, apikey = apikey)
        self.client = openai.OpenAI(
            api_key = self.apikey, base_url = base_url
        )


    def generate(self, request : AIRequest) -> AIResponse:
        """
        Generate Content via the OpenAI/Base URL (NVDIA-NIM/etc.) API
        """

        start = time.monotonic()

        # ! context holds the rendered Jinja2 template — send it as the system
        # ! message so the model follows the markdown/structure instructions;
        # ! without this the template is silently dropped and never seen by the API
        messages : list[dict] = []
        if request.context:
            messages.append({"role" : "system", "content" : request.context})
        messages.append({"role" : "user", "content" : request.prompt})

        try:
            response = self.client.chat.completions.create(
                model       = self.model.model,
                max_tokens  = self.model.max_tokens,
                temperature = self.model.temperature,
                messages    = messages,
            )
        except openai.RateLimitError as e:
            raise AIRateLimitError(f"Rate Limit Reached: {e}") from e
        except openai.APIError as e:
            raise AIClientError(f"Claude API Error: {e}") from e

        latency = time.monotonic() - start
        raw_response = response.choices[0].message.content \
            if response.choices else None # failed to get any response
        
        print(
            f"VERBOSE: ClaudeClient.generate({request.topic[:40]}...)"
        )

        return AIResponse(
            request_id = request.request_id or str(uuid.uuid4()),
            raw_response = raw_response,
            in_tokens = response.usage.prompt_tokens,
            out_tokens = response.usage.completion_tokens,
            latency = latency
        )
