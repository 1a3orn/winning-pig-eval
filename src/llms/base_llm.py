from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLM(ABC):
    def __init__(
        self,
        api_key: str,
        temperature: float = 0.85,
        max_tokens: int = 8192,
    ):
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    async def __call__(
        self,
        messages: List[Dict[str, Any]],
        **kwargs
    ) -> str:
        """Make a request to the LLM API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Generated text response
            
        Raises:
            ValueError: If messages format is invalid
        """
        pass

    def validate_messages(self, messages: List[Dict[str, Any]], valid_roles: set) -> None:
        """Validate message format.
        
        Args:
            messages: List of message dictionaries
            valid_roles: Set of allowed role values
            
        Raises:
            ValueError: If message format is invalid
        """
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError(f"Each message must be a dictionary, got {type(msg)}")
            if 'role' not in msg or 'content' not in msg:
                raise ValueError("Each message must contain 'role' and 'content' keys")
            if not isinstance(msg['role'], str) or not isinstance(msg['content'], str):
                raise ValueError("Message 'role' and 'content' must be strings")
            if msg['role'] not in valid_roles:
                raise ValueError(f"Message role must be one of {valid_roles}, got '{msg['role']}'")