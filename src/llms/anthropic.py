import anthropic
from typing import List, Dict, Any, Optional

class AnthropicAPI:
    def __init__(
        self, 
        api_key: str, 
        temperature: float = 0.85,
        max_tokens: int = 8192,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.temperature = temperature
        self.model = model
        self.max_tokens = max_tokens
    async def __call__(self, messages: List[Dict[str, Any]]):
        # Peel off the system prompt if it exists.
        system_prompt = None
        if len(messages) > 0 and messages[0]["role"] == "system":
            system_prompt = messages[0]["content"]
            messages = messages[1:]
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            system=system_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        txt = response.content[0].text
        return txt
