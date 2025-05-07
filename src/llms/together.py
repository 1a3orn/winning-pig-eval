from together import Together
from typing import List, Dict, Any
from llms.base_llm import BaseLLM
import requests

class TogetherAPI(BaseLLM):
    def __init__(
        self,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: int = 31000,
        model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    ):
        super().__init__(api_key, temperature, max_tokens)
        self.key = api_key
        self.model = model

    async def __call__(self, messages: List[Dict[str, Any]]):
        self.validate_messages(messages, {'system', 'user', 'assistant'})

        client = Together(api_key=self.key)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        text = response.choices[0].message.content
        return text