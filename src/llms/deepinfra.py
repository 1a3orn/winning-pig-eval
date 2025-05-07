from openai import OpenAI
from typing import List, Dict, Any, Optional
from llms.base_llm import BaseLLM

class DeepInfraAPI(BaseLLM):
    def __init__(
        self,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: int = 40000,
        model: str = "Qwen/Qwen3-30B-A3B"
    ):
        super().__init__(api_key, temperature, max_tokens)
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepinfra.com/v1/openai/"
        )
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    async def __call__(self, messages: List[Dict[str, Any]], **kwargs):
        self.validate_messages(messages, {'system', 'user', 'assistant'})
        
        print("Sending request to DeepInfra")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content