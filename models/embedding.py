import torch
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, cfg):
        device = self._select_device()
        print(f"Embedding Device : {device}")
        self.model = SentenceTransformer(
            cfg.embedding.model,
            device=device,
        )

    def _select_device(self):
        if torch.cuda.is_available():
            return "cuda"

        if torch.backends.mps.is_available():
            return "mps"

        return "cpu"

    def encode(self, text):
        return self.model.encode(
            text,
            normalize_embeddings=True,
        )

    def encode_batch(self, texts):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )