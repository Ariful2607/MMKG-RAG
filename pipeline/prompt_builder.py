class PromptBuilder:

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
You are a helpful AI assistant specialized in question answering over a knowledge graph.

Your task is to answer the user's question ONLY using the provided context.

Rules:
- Use only the information in the context.
- Do not hallucinate.
- If the answer is not contained in the context, reply:
"I don't know based on the provided context."

----------------------------------------
Context

{context}

----------------------------------------

Question:
{question}

Answer:
"""

        return prompt.strip()