import torch

from transformers import (
    AutoProcessor,
    Qwen2_5_VLForConditionalGeneration,
)

from models.base_model import BaseModel

class QwenVLModel(BaseModel):
    def __init__(self, cfg):
        self.cfg = cfg
        print("Loading Qwen2.5-VL...")

        self.processor = AutoProcessor.from_pretrained(
            cfg.vlm.model
        )

        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            cfg.vlm.model,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        print("Model Loaded.")

    def generate(self, image=None, text=None, prompt=""):
        raise NotImplementedError