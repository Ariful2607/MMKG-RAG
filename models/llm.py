from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LLM:

    def __init__(self, cfg):

        self.provider = cfg.llm.provider
        self.model_name = cfg.llm.model

        if self.provider == "huggingface":

            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
            )

        else:
            raise ValueError(
                f"Unsupported provider: {self.provider}"
            )

    def generate(
        self,
        prompt,
        max_new_tokens=512,
    ):

        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
        )

        response = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True,
        )

        return response.strip()