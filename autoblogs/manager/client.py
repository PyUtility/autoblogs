# -*- encoding: utf-8 -*-

"""
A Application for Management of Clients for AutoBlogs
"""

from typing import Dict, Optional, Callable

from autoblogs.error.error import AIClientError
from autoblogs.config.constants import AIProvider

class ClientManager(object):
    """
    Abstract AI Client Interface for Content Generation

    The abstract class provides a built-in default class ``generate``
    that can be used uniformly across any concrete models. The
    abstract methods provide default signature which is enforced to
    remain the same in the concrete classes.

    :type  provider: str
    :param provider: Name of the supported AI/LLM Agents provider(s),
        this can be any of the defined :class:`AIProvider` values. A
        provider may require Python specific SDK module - for example
        when using ``CLAUDE`` the ``anthropic`` module is required, or
        ``openai`` is required for ``OPENAI`` or ``NVIDIA-NIM``. The
        client manager checks if the existing model is present and
        raises an exception if not.

    :type  modelname: str
    :param modelname: Any valid name of the model, this is a string
        and can be customized as per the provider. Check individual
        providers for the list of supported models.

    :type  apikey: Optional[str]
    :param apikey: API Key for the AI Provider, this should be defined
        under the environment variable.

    :type  base_url: str
    :param base_url: Some models like ``NVIDIA-NIM`` requires a custom
        base URL which calls the underlying APIs. The URL is passed
        to the underlying client functions as a parameter.
    """

    def __init__(
            self,
            provider : str,
            modelname : str,
            apikey : Optional[str] = None,
            base_url : Optional[str] = None
    ) -> None:
        self.provider = self.__set_provider__(provider = provider)
        self.modelname = modelname
        self.apikey = apikey
        self.base_url = base_url


    @property
    def defaultSDK(self) -> Dict[str, str]:
        return {
            "CLAUDE" : "anthropic", "OPENAI" : "openai",
            "NVIDIA-NIM" : "openai", "LOCAL" : "openai"
        }


    @property
    def client(self) -> Callable:
        _provider = self.provider.value

        if _provider == "CLAUDE":
            from autoblogs.client.anthropic import claudeGenerate
            _client = claudeGenerate
        else:
            from autoblogs.client.openai import generateOpenAI
            _client = generateOpenAI

        return _client


    def __set_provider__(self, provider : str) -> AIProvider:
        _provider = AIProvider.getName(name = provider)
        clientsdk = self.defaultSDK[_provider.value] # type: ignore

        try:
            __import__(clientsdk)
        except ImportError:
            raise AIClientError(f"PySDK `{clientsdk}` is Required.")
        
        return _provider
