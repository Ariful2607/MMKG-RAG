from openai import OpenAI
from models.base_llm import BaseLLM
from models.response import LLMResponse
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAILLM(BaseLLM):
    def __init__(self, model):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = model
    
    def generate(
        self,
        prompt: str,
    ):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )
        msg = response.choices[0].message.content
        return LLMResponse(
            text=msg,
            model=self.model,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
        )