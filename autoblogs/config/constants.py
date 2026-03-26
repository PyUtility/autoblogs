# -*- encoding: utf-8 -*-

"""
A Set of Typical Application-Wide Constants Defined as ENUM

An constant is a value that is set application-wide to process values
and to change the state of the application based on a certain values.
The typical constants are defined as below:

    * :class:`DraftState` - Content draft lifecycle state machine
        values. This define a content can go through multiple rounds
        of refinement and can only be part of any one of the value.

    * :class:`AIProvider` - A set of available AI/LLM agent provider
        where a client is available and supported/tested.
"""

from enum import Enum

DraftState = Enum(
    "DraftState", [
        "PENDING", "GENERATING", "DRAFT", "REVIEWING", "APPROVED",
        "PUBLISHED", "FAILED", "RETRACTED", "DELETED"
    ]
)


AIProvider = Enum(
    "AIProvider", ["CLAUDE", "OPENAI", "NVIDIA_NIM", "LOCAL"]
)

# LLM Agent Specific Model Name(s); Useful for Context Setting and
# other forms of optimization of the output, token usage, etc.
ClaudeModel = Enum(
    "ClaudeModel", ["HAIKU 4.5", "SONET 4.6", "OPUS 4.6"],
)

OpenAIModel = Enum(
    "OpenAIModel", ["GPT-5.1 Codex", "GPT-4.1", "GPT-5 nano"]
)
