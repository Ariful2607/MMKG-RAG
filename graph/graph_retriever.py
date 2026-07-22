from utils.similarity import cosine_similarity

class GraphRetriever:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def retrieve(
        self,
        graph,
        question,
        top_k=5,
    ):
        print("\n========== Graph Retrieval ==========")
        query_embedding = self.embedding_model.encode(question)
        results = []

        for entity in graph.entities.values():
            if entity.embedding is None:
                continue

            score = cosine_similarity(
                query_embedding,
                entity.embedding,
            )
            results.append(
                (
                    entity,
                    float(score),
                )
            )

        results.sort(
            key=lambda x: x[1],
            reverse=True,
        )
        return results[:top_k]