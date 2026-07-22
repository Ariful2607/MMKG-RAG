from graph.graph import KnowledgeGraph

class NeighborExpander:
    def __init__(self):
        pass

    def expand(
        self,
        graph: KnowledgeGraph,
        retrieved_entities,
    ):
        expanded_entities = {}
        expanded_relations = []
        for entity, score in retrieved_entities:
            expanded_entities[entity.id] = entity

        for entity in list(expanded_entities.values()):
            for neighbor_id in graph.graph.neighbors(entity.id):
                neighbor = graph.entities[neighbor_id]
                expanded_entities[neighbor.id] = neighbor
                edge_dict = graph.graph.get_edge_data(
                    entity.id,
                    neighbor_id,
                )
                for edge in edge_dict.values():
                    expanded_relations.append(edge["relation_obj"])

            for parent_id in graph.graph.predecessors(entity.id):
                parent = graph.entities[parent_id]
                expanded_entities[parent.id] = parent
                edge_dict = graph.graph.get_edge_data(
                    parent_id,
                    entity.id,
                )
                for edge in edge_dict.values():
                    expanded_relations.append(edge["relation_obj"])

        return {
            "entities": list(expanded_entities.values()),
            "relations": expanded_relations,
        }