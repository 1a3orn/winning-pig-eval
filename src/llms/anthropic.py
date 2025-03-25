import anthropic
from typing import List, Dict, Any, Optional
from llms.base_llm import BaseLLM

class AnthropicAPI(BaseLLM):
    def __init__(
        self, 
        api_key: str, 
        temperature: float = 0.85,
        max_tokens: int = 8192,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        super().__init__(api_key, temperature, max_tokens)
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    async def __call__(self, messages: List[Dict[str, Any]], **kwargs):
        self.validate_messages(messages, {'system', 'user', 'assistant'})
        
        # Peel off the system prompt if it exists.
        system_prompt = None
        if len(messages) > 0 and messages[0]["role"] == "system":
            system_prompt = messages[0]["content"]
            messages = messages[1:]
        
        # Throw if we have a system prompt but no messages
        if system_prompt and len(messages) == 0:
            raise ValueError("No messages provided")
        
        # Throw if system prompt is not in the first message
        if any(message["role"] == "system" for message in messages):
            raise ValueError("System prompt must be in the first message")
        
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            system=system_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.content[0].text
