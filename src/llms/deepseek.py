import asyncio
from typing import List, Dict, Any, Optional
from aiohttp import ClientSession
import json
from asyncio import Semaphore

from llms.base_llm import BaseLLM

class DeepseekAPI(BaseLLM):
    def __init__(
        self, 
        api_key: str,
        base_url: str = "https://api.deepseek.com/v1/chat/completions",
        concurrent_limit: int = 10,
        temperature: float = 0.85,
        max_tokens: int = 8000,
        model: str = "deepseek-chat"
    ):
        """Initialize the Deepseek API client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API endpoint
            concurrent_limit: Maximum number of concurrent API calls allowed
        """
        super().__init__(api_key, temperature, max_tokens)
        self.base_url = base_url
        self.model = model
        self._semaphore = Semaphore(concurrent_limit)
        self._session: Optional[ClientSession] = None

    async def _ensure_session(self) -> ClientSession:
        """Ensure an aiohttp session exists and return it."""
        if self._session is None or self._session.closed:
            self._session = ClientSession(headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
        return self._session

    async def __call__(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """Make a request to the Deepseek API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model identifier to use
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            API response as a string
            
        Raises:
            ValueError: If messages format is invalid
        """
        self.validate_messages(messages, {'system', 'user', 'assistant'})
        
        async with self._semaphore:
            session = await self._ensure_session()
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                **kwargs
            }
            
            async with session.post(self.base_url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {error_text}")
                values = await response.json()
                return values['choices'][0]['message']['content']

    async def close(self):
        """Close the API client session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        """Support async context manager protocol."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting context."""
        await self.close()