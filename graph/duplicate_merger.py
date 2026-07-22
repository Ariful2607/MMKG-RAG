import re
from collections import defaultdict

class DuplicateMerger:
    def normalize(self, text: str) -> str:
        text = text.lower()

        # remove extra spaces
        text = re.sub(r"\s+", " ", text)

        # remove surrounding spaces
        text = text.strip()

        # remove parentheses
        text = re.sub(r"\((.*?)\)", "", text)

        # remove punctuation
        text = re.sub(r"[^\w\s]", "", text)

        # singular
        if text.endswith("s"):
            text = text[:-1]

        return text.strip()

    def build_groups(self, graph):
        groups = defaultdict(list)
        for entity in graph.entities.values():
            key = self.normalize(entity.name)
            groups[key].append(entity)

        return groups

    def merge_group(self, graph, entities):
        if len(entities) <= 1:
            return

        keep = entities[0]
        for duplicate in entities[1:]:
            # redirect outgoing edges
            for _, target, key, data in list(
                graph.graph.out_edges(
                    duplicate.id,
                    keys=True,
                    data=True,
                )
            ):
                graph.graph.add_edge(
                    keep.id,
                    target,
                    **data,
                )

            # redirect incoming edges
            for source, _, key, data in list(
                graph.graph.in_edges(
                    duplicate.id,
                    keys=True,
                    data=True,
                )
            ):
                graph.graph.add_edge(
                    source,
                    keep.id,
                    **data,
                )
            graph.graph.remove_node(duplicate.id)
            del graph.entities[duplicate.id]

    def merge(self, graph):
        groups = self.build_groups(graph)
        total = 0
        for entities in groups.values():
            before = len(entities)
            self.merge_group(graph, entities)
            total += before - 1

        print(f"Merged {total} duplicate entities.")