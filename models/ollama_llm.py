from ollama import Client
from models.base_llm import BaseLLM
from models.response import LLMResponse

class OllamaLLM(BaseLLM):
    def __init__(self, model):
        self.client = Client()
        self.model = model

    def generate(self, prompt):
        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return LLMResponse(
            text=response["message"]["content"],
            model=self.model,
        )