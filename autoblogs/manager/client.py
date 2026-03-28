# -*- encoding: utf-8 -*-

"""
A Application for Management of Clients for AutoBlogs
"""

from typing import Optional, Callable

from autoblogs.config.constants import (
    AIProvider, ClaudeModel, OpenAIModel
)
from autoblogs.error import UndefinedModel
from autoblogs.model.dataflows import AIModel
from autoblogs.config.constants import AIProvider

class ClientManager(object):
    """
    Abstract AI Client Interface for Content Generation

    The abstract class provides a built-in default class ``generate``
    that can be used uniformly across any concrete models. The
    abstract methods provide default signature which is enforced to
    remain the same in the concrete classes.

    :type  apikey: str
    :param apikey: API Key for the AI Provider, this should be defined
        under the environment variable.
    """

    def __init__(self, apikey : Optional[str]) -> None:
        self.apikey = apikey # any valid key, or none if not required

        # Set AI Provider based on User Input/UI Calls (TODO)
        self.provider = self.__set_provider__()

        # Set the Client Engine based on the Provider Name
        self.client = self.__set_client__(provider = self.provider)

        # Set the Model Name based on the Provider Name
        self.model = self.__set_model__(provider = self.provider)

        # Set other Model Controls (TODO Method) for Inputs
        self.max_tokens = int(input("Max. Tokens [4096]: ") or 4096)
        self.temperature = float(input("Temperature [0.7]: ") or 0.7)


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
    

    def __set_client__(self, provider : AIProvider) -> Callable:
        requirements = dict(CLAUDE = "anthropic")
        requirements = requirements.get(provider.name, "openai")

        # check hard dependency for the module; else raise error
        # this should be adjusted with the AI Client Error Module
        try:
            __import__(requirements)
        except ImportError:
            raise ImportError(
                f"Required Module {requirements} is not installed"
            )
        
        # based on the provider, return the client name with import
        if provider == "CLAUDE":
            from autoblogs.client.anthropic import claudeGenerate
            client = claudeGenerate
        else:
            from autoblogs.client.openai import generateOpenAI
            client = generateOpenAI

        return client


    def __set_model__(self, provider : AIProvider) -> Optional[str]:
        models = dict(CLAUDE = ClaudeModel, OPENAI = OpenAIModel)
        models = models.get(provider.name, None)

        model = None # only when LOCAL/custom model is required
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
                
                model = model.name
            except (KeyError, ValueError):
                model = selection.upper()
        else:
            model = "https://localhost:11434"

        return model
