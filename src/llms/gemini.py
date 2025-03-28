from openai import OpenAI
from typing import List, Dict, Any, Optional
from llms.base_llm import BaseLLM

class GeminiAPI(BaseLLM):
    def __init__(
        self,
        api_key: str,
        temperature: float = 0.6,
        max_tokens: int = 8192,
        model: str = "gemini-2.5-pro-exp-03-25"
    ):
        super().__init__(api_key, temperature, max_tokens)
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = model

    async def __call__(self, messages: List[Dict[str, Any]], **kwargs):
        self.validate_messages(messages, {'system', 'user', 'assistant'})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content