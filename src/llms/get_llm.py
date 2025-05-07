import os

from llms.base_llm import BaseLLM
from llms.deepseek import DeepseekAPI
from llms.anthropic import AnthropicAPI
from llms.openai import OpenAIAPI
from llms.human_terminal import HumanTerminal
from llms.gemini import GeminiAPI
from llms.together import TogetherAPI
from llms.deepinfra import DeepInfraAPI
from llms.fireworks import FireworksAPI

def get_llm(
    model: str,
    temperature: float = 0.7
) -> BaseLLM:

    if model.startswith("anthropic:"):
        llm = AnthropicAPI(
            os.getenv("ANTHROPIC_API_KEY"),
            temperature=temperature,
            model=model.split(":")[1]
        )
    elif model.startswith("deepseek:"):
        llm = DeepseekAPI(
            os.getenv("DEEPSEEK_API_KEY"),
            temperature=temperature,
            model=model.split(":")[1]
        )
    elif model.startswith("openai:"):
        llm = OpenAIAPI(
            os.getenv("OPENAI_API_KEY"),
            temperature=temperature,
            model=model.split(":")[1]
        )
    elif model.startswith("together:"):
        llm = TogetherAPI(
            os.getenv("TOGETHER_API_KEY"),
            temperature=temperature,
            model=model.split(":")[1]
        )
    elif model.startswith("gemini:"):
        llm = GeminiAPI(
            os.getenv("GEMINI_API_KEY"),
            temperature=temperature,
            model=model.split(":")[1]
        )
    elif model.startswith("deepinfra:"):
        llm = DeepInfraAPI(
            os.getenv("DEEPINFRA_API_KEY"),
            temperature=temperature,
            model=model.split(":")[1]
        )
    elif model.startswith("fireworks:"):
        llm = FireworksAPI(
            os.getenv("FIREWORKS_API_KEY"),
            temperature=temperature,
            model=model.split(":")[1]
        )
    elif model == 'human_terminal':
        llm = HumanTerminal()
    else:
        raise ValueError(f"Invalid model: {model}")

    return llm
