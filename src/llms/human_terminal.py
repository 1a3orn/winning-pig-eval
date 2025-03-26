from typing import List, Dict, Any
from llms.base_llm import BaseLLM

class HumanTerminal(BaseLLM):
    def __init__(
        self,
        api_key: str = "not_needed",
        temperature: float = 0.85,
        max_tokens: int = 8192,
    ):
        super().__init__(api_key, temperature, max_tokens)

    async def __call__(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        self.validate_messages(messages, {'system', 'user', 'assistant'})
        
        # Print all messages in sequence
        print("\n=== Conversation History ===")
        for msg in messages:
            role = msg["role"].upper()
            content = msg["content"]
            print(f"\n[{role}]:\n{content}")
            
        print("\n=== Your Response ===")
        data = input()
        
        return data
