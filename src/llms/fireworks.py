import asyncio
from typing import List, Dict, Any, Optional
from aiohttp import ClientSession
import json

from llms.base_llm import BaseLLM

class FireworksAPI(BaseLLM):
    def __init__(
        self,
        api_key: str,
        temperature: float = 0.6,
        max_tokens: int = 16000,
        model: str = "accounts/fireworks/models/qwen3-235b-a22b",
        top_p: float = 1.0,
        top_k: int = 40,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
    ):
        super().__init__(api_key, temperature, max_tokens)
        self.model = model
        self.top_p = top_p
        self.top_k = top_k
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.base_url = "https://api.fireworks.ai/inference/v1/chat/completions"
        self._session: Optional[ClientSession] = None

    async def _ensure_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession(headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            })
        return self._session

    async def __call__(
        self,
        messages: List[Dict[str, Any]],
        **kwargs
    ) -> str:
        self.validate_messages(messages, {'system', 'user', 'assistant'})

        should_close_session = self._session is None
        session = await self._ensure_session()

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "temperature": self.temperature,
            "messages": messages
        }
        payload.update(kwargs)

        try:
            async with session.post(self.base_url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Fireworks API request failed: {error_text}")
                values = await response.json()
                text = values['choices'][0]['message']['content']
                #print(text[-20:])
                return text
        finally:
            if should_close_session:
                await self.close()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
