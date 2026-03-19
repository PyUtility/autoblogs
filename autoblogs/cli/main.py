# -*- encoding: utf-8 -*-

"""
CLI Application for AutoBlogs - Content Creation Tool
"""

import getpass

from autoblogs.prompts import PROMPT_BLOGS
from autoblogs.client.openai import OpenAIClient
from autoblogs.model.dataflows import AIModel, AIRequest, AIResponse

topic = input("Topic: ")
prompt = input("One Line Prompt: ")
apikey = getpass.getpass("API Key: ")

def launch() -> AIResponse:
    model = AIModel(
        model = "nvidia/nemotron-content-safety-reasoning-4b"
    )
    request = AIRequest(
        topic = topic, prompt = prompt, context = PROMPT_BLOGS
    )

    client = OpenAIClient(
        model = model, apikey = apikey,
        base_url = "https://integrate.api.nvidia.com/v1"
    )

    response = client.generate(request = request)
    print(response.raw_response)

    return response

if __name__ == "__main__":
    launch()
