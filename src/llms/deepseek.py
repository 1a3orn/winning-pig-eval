import asyncio
from typing import List, Dict, Any, Optional
from aiohttp import ClientSession
import json
from asyncio import Semaphore

class DeepseekAPI:
    def __init__(
        self, 
        api_key: str,
        base_url: str = "https://api.deepseek.com/v1/chat/completions",
        concurrent_limit: int = 10,
        temperature: float = 0.85
    ):
        """Initialize the Deepseek API client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API endpoint
            concurrent_limit: Maximum number of concurrent API calls allowed
        """
        self.api_key = api_key
        self.base_url = base_url
        self._semaphore = Semaphore(concurrent_limit)
        self._session: Optional[ClientSession] = None
        self.temperature = temperature
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
        model: str = "deepseek-chat",
        temperature = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make a request to the Deepseek API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model identifier to use
            temperature: Sampling temperature (0.0 to 1.0)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            API response as a dictionary
            
        Raises:
            ValueError: If messages format is invalid
        """
        if temperature is None:
            temperature = self.temperature
        # Validate messages format
        valid_roles = {'system', 'user', 'assistant'}
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError(f"Each message must be a dictionary, got {type(msg)}")
            if 'role' not in msg or 'content' not in msg:
                raise ValueError("Each message must contain 'role' and 'content' keys")
            if not isinstance(msg['role'], str) or not isinstance(msg['content'], str):
                raise ValueError("Message 'role' and 'content' must be strings")
            if msg['role'] not in valid_roles:
                raise ValueError(f"Message role must be one of {valid_roles}, got '{msg['role']}'")

        async with self._semaphore:
            session = await self._ensure_session()
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 8000,
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