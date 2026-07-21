from models.qwen_vl import QwenVLModel

def create_model(cfg):
    provider = cfg.vlm.provider
    if provider == "huggingface":
        return QwenVLModel(cfg)
    raise ValueError(f"Unknown provider: {provider}")