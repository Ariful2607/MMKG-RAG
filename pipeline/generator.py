from pipeline.prompt_builder import PromptBuilder


class Generator:

    def __init__(
        self,
        llm,
    ):
        self.llm = llm
        self.prompt_builder = PromptBuilder()

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = self.prompt_builder.build(
            question=question,
            context=context,
        )

        answer = self.llm.generate(prompt)

        return answer