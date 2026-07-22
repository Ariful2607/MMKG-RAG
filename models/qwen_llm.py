import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from models.base_model import BaseModel
from models.response import ModelResponse


class QwenLLM(BaseModel):
    """Local Hugging Face wrapper for Qwen text-only generation."""

    def __init__(self, cfg):
        self.cfg = cfg

        print("Loading Qwen2.5 text LLM...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            cfg.llm.model
        )

        torch_dtype = self._select_dtype()

        self.model = AutoModelForCausalLM.from_pretrained(
            cfg.llm.model,
            torch_dtype=torch_dtype,
            device_map="auto",
        )

        self.model.eval()
        self.device = next(self.model.parameters()).device

        print(f"Device : {self.device}")
        print(f"DType  : {torch_dtype}")
        print("LLM Loaded.")

    def _select_dtype(self):
        dtype_cfg = self.cfg.llm.get("dtype", "auto")

        if dtype_cfg != "auto":
            return getattr(torch, dtype_cfg)

        if torch.cuda.is_available():
            return torch.bfloat16

        if torch.backends.mps.is_available():
            return torch.float16

        return torch.float32

    def generate(self, prompt: str) -> ModelResponse:
        """Generate a deterministic answer from a text prompt."""
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        chat = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            chat,
            return_tensors="pt",
        ).to(self.device)

        max_new_tokens = self.cfg.llm.get(
            "max_new_tokens",
            512,
        )

        with torch.inference_mode():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated_ids = output_ids[
            :,
            inputs.input_ids.shape[1]:,
        ]

        response_text = self.tokenizer.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0].strip()

        return ModelResponse(text=response_text)