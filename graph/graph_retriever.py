from utils.similarity import cosine_similarity


class GraphRetriever:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def retrieve(
        self,
        graph,
        question: str,
        top_k: int = 5,
    ):

        print("\n========== Graph Retrieval ==========")

        # Encode question
        question_embedding = self.embedding_model.encode(question)

        results = []

        for entity in graph.entities.values():

            if entity.embedding is None:
                continue

            score = cosine_similarity(
                question_embedding,
                entity.embedding,
            )

            results.append((entity, score))

        results.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        results = results[:top_k]

        print()

        for i, (entity, score) in enumerate(results, start=1):
            print(
                f"{i:02d}. "
                f"{entity.name:<40}"
                f"{score:.4f}"
            )

        return results