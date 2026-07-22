from collections import deque

from graph.graph import KnowledgeGraph


class NeighborExpander:

    def expand(
        self,
        graph,
        retrieval_results,
        hops=1,
        max_neighbors=None,
    ):

        print("\n========== Neighbor Expansion ==========")

        subgraph = KnowledgeGraph()

        visited = set()
        queue = deque()

        ####################################################
        # Initialize queue
        ####################################################

        for entity, _ in retrieval_results:

            subgraph.add_entity(entity)

            visited.add(entity.id)

            queue.append((entity.id, 0))

        ####################################################
        # BFS
        ####################################################

        while queue:

            node_id, depth = queue.popleft()

            if depth >= hops:
                continue

            neighbors = []

            ####################################################
            # Outgoing edges
            ####################################################

            for _, neighbor_id, edge_data in graph.graph.out_edges(
                node_id,
                data=True,
            ):
                neighbors.append(
                    (
                        neighbor_id,
                        edge_data["relation_obj"],
                    )
                )

            ####################################################
            # Incoming edges
            ####################################################

            for neighbor_id, _, edge_data in graph.graph.in_edges(
                node_id,
                data=True,
            ):
                neighbors.append(
                    (
                        neighbor_id,
                        edge_data["relation_obj"],
                    )
                )

            ####################################################
            # Sort by confidence
            ####################################################

            neighbors.sort(
                key=lambda x: x[1].confidence,
                reverse=True,
            )

            ####################################################
            # Limit neighbors
            ####################################################

            if max_neighbors is not None:
                neighbors = neighbors[:max_neighbors]

            ####################################################
            # Expand
            ####################################################

            for neighbor_id, relation in neighbors:

                neighbor = graph.entities[neighbor_id]

                # Add entity
                subgraph.add_entity(neighbor)

                # Add relation
                subgraph.add_relation(relation)

                # Continue BFS
                if neighbor.id not in visited:

                    visited.add(neighbor.id)

                    queue.append(
                        (
                            neighbor.id,
                            depth + 1,
                        )
                    )

        print(subgraph.statistics())

        return subgraph