import os

from llms.base_llm import BaseLLM
from llms.deepseek import DeepseekAPI
from llms.anthropic import AnthropicAPI
from llms.openai import OpenAIAPI

def get_llm(
    model: str,
    temperature: float = 0.6
) -> BaseLLM:

    if 'claude' in model:
        llm = AnthropicAPI(
            os.getenv("ANTHROPIC_API_KEY"),
            temperature=temperature,
            model=model
        )
    elif 'deepseek' in model:
        llm = DeepseekAPI(
            os.getenv("DEEPSEEK_API_KEY"),
            temperature=temperature,
            model=model
        )
    elif 'gpt' in model or 'o1' in model or 'o3' in model:
        llm = OpenAIAPI(
            os.getenv("OPENAI_API_KEY"),
            temperature=temperature,
            model=model
        )
    else:
        raise ValueError(f"Invalid model: {model}")

    return llm
