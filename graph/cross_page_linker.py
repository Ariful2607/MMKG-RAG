from graph.relation import Relation
from utils.similarity import cosine_similarity


class CrossPageLinker:
    def __init__(self, threshold: float = 0.90):
        self.threshold = threshold

    def link(self, graph):
        print("\n========== Cross Page Linking ==========")
        entities = list(graph.entities.values())
        added = 0
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i + 1:]:

                # --------------------------
                # Skip same page
                # --------------------------
                if entity1.source_page == entity2.source_page:
                    continue

                # --------------------------
                # Skip different types
                # --------------------------
                if entity1.entity_type != entity2.entity_type:
                    continue

                # --------------------------
                # Skip missing embedding
                # --------------------------
                if entity1.embedding is None:
                    continue

                if entity2.embedding is None:
                    continue

                # --------------------------
                # Cosine similarity
                # --------------------------
                score = cosine_similarity(
                    entity1.embedding,
                    entity2.embedding,
                )

                if score < self.threshold:
                    continue

                if graph.has_relation(
                    entity1.id,
                    entity2.id,
                    "same_as",
                ):
                    continue

                relation = Relation(
                    source=entity1.id,
                    target=entity2.id,
                    relation="same_as",
                    description="Semantic cross-page link",
                    confidence=float(score),
                    source_page=-1,
                )

                graph.add_relation(relation)

                added += 1

                print(
                    f"[LINK] "
                    f"{entity1.name}"
                    f" <--> "
                    f"{entity2.name}"
                    f" ({score:.3f})"
                )

        print(f"\nAdded {added} semantic links.")

