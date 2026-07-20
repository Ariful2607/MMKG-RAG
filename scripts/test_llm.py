from models.ollama_llm import OllamaLLM

llm = OllamaLLM("qwen2.5:7b")

response = llm.generate(
    "Explain what is Transformer in one sentence."
)

print(response.text)