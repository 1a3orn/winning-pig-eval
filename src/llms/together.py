from typing import List, Dict, Any
from llms.base_llm import BaseLLM

class TogetherAPI(BaseLLM):
    def __init__(
        self,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    ):
        super().__init__(api_key, temperature, max_tokens)
        self.key = api_key
        self.model = model

    async def __call__(self, messages: List[Dict[str, Any]]):
        self.validate_messages(messages, {'system', 'user', 'assistant'})
        
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.together.xyz/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"API request failed with status {response.status}")
                data = await response.json()
                text = data['choices'][0]['message']['content']
                return text