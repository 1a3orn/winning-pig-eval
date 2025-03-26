import asyncio
from typing import List, Dict, Any, Optional
from aiohttp import ClientSession
import json

from llms.base_llm import BaseLLM

class DeepseekAPI(BaseLLM):
    def __init__(
        self, 
        api_key: str,
        temperature: float = 0.85,
        max_tokens: int = 8192,  # Changed to match Anthropic's default
        model: str = "deepseek-chat"
    ):
        """Initialize the Deepseek API client.
        
        Args:
            api_key: API key for authentication
        """
        super().__init__(api_key, temperature, max_tokens)
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = model
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
        messages: List[Dict[str, Any]],  # Changed to match Anthropic's type hint
        **kwargs
    ) -> str:
        """Make a request to the Deepseek API."""
        self.validate_messages(messages, {'system', 'user', 'assistant'})
        
        # Handle system prompt like Anthropic
        system_prompt = None
        if len(messages) > 0 and messages[0]["role"] == "system":
            system_prompt = messages[0]["content"]
            messages = messages[1:]
        
        if system_prompt and len(messages) == 0:
            raise ValueError("No messages provided")
            
        if any(message["role"] == "system" for message in messages):
            raise ValueError("System prompt must be in the first message")

        # Create a new session for each call if none exists
        should_close_session = self._session is None
        session = await self._ensure_session()
        
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            # Add system prompt to payload if it exists
            if system_prompt:
                payload["system"] = system_prompt
                
            # Add any additional kwargs
            payload.update(kwargs)
            
            async with session.post(self.base_url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {error_text}")
                values = await response.json()
                return values['choices'][0]['message']['content']
        finally:
            if should_close_session:
                await self.close()

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