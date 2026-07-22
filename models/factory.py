from models.qwen_vl import QwenVLModel
from models.embedding import EmbeddingModel

def create_model(cfg):
    provider = cfg.vlm.provider
    if provider == "huggingface":
        return QwenVLModel(cfg)
    raise ValueError(f"Unknown provider: {provider}")

def create_embedding(cfg):
    return EmbeddingModel(cfg)