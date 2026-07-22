from graph.graph import KnowledgeGraph


class NeighborExpander:

    def expand(
        self,
        graph,
        retrieval_results,
    ):

        print("\n========== Neighbor Expansion ==========")

        subgraph = KnowledgeGraph()

        visited = set()

        ####################################################
        # copy retrieved entities
        ####################################################

        for entity, _ in retrieval_results:

            subgraph.add_entity(entity)

            visited.add(entity.id)

        ####################################################
        # expand neighbors
        ####################################################

        for entity, _ in retrieval_results:

            for _, neighbor_id, edge_data in graph.graph.out_edges(
                entity.id,
                data=True,
            ):

                neighbor = graph.entities[neighbor_id]

                if neighbor.id not in visited:

                    subgraph.add_entity(neighbor)

                    visited.add(neighbor.id)

                relation = edge_data["relation_obj"]

                subgraph.add_relation(relation)

            for neighbor_id, _, edge_data in graph.graph.in_edges(
                entity.id,
                data=True,
            ):

                neighbor = graph.entities[neighbor_id]

                if neighbor.id not in visited:

                    subgraph.add_entity(neighbor)

                    visited.add(neighbor.id)

                relation = edge_data["relation_obj"]

                subgraph.add_relation(relation)

        print(subgraph.statistics())

        return subgraph