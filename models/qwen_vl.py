import torch
from qwen_vl_utils import process_vision_info
from models.response import ModelResponse
from PIL import Image
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

        self.device = next(self.model.parameters()).device
        print("Model Loaded.")

    def generate(self, image, text="", prompt=""):
        img = Image.open(image).convert("RGB")
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": img,
                    },
                    {
                        "type": "text",
                        "text": f"{prompt}\n\nPage Text:\n{text}",
                    },
                ],
            }
        ]

        chat = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        image_inputs, video_inputs = process_vision_info(messages)

        inputs = self.processor(
            text=chat,
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )

        inputs = inputs.to(self.device)

        with torch.inference_mode():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=1024,
            )

        generated_ids = [
            output[len(input_ids):]
            for input_ids, output in zip(inputs.input_ids, output_ids)
        ]

        response = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]

        return ModelResponse(text=response)