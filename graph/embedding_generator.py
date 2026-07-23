from typing import List
from graph.graph import KnowledgeGraph
from models.embedding import EmbeddingModel

class EmbeddingGenerator:
    """
    Generate semantic embeddings for every entity in the knowledge graph.
    """

    def __init__(self, embedding_model: EmbeddingModel):
        self.embedding_model = embedding_model

    def build_text(self, entity) -> str:
        """
        Build the semantic representation of an entity.
        """
        parts = [
            f"Name: {entity.name}",
            f"Type: {entity.entity_type}",
        ]

        if entity.description:
            parts.append(f"Description: {entity.description}")

        if entity.caption:
            parts.append(f"Caption: {entity.caption}")

        return "\n".join(parts)

    def generate(self, graph: KnowledgeGraph):
        print("\n========== Generating Entity Embeddings ==========")
        entities = list(graph.entities.values())
        texts = [
            self.build_text(entity)
            for entity in entities
        ]
        embeddings = self.embedding_model.encode_batch(texts)

        for entity, embedding in zip(entities, embeddings):

            # store inside entity
            entity.embedding = embedding.tolist()

        print(f"Generated embeddings for {len(entities)} entities.")