import networkx as nx
from graph import relation
from graph.entity import Entity
from graph.relation import Relation

class KnowledgeGraph:
    def __init__(self):
        self.entities = {}
        self.relations = []
        self.graph = nx.MultiDiGraph()

    # Entity
    def add_entity(self, entity: Entity):
        if entity.id in self.entities:
            return

        self.entities[entity.id] = entity

        self.graph.add_node(
            entity.id,
            name=entity.name,
            entity_type=entity.entity_type,
            description=entity.description,
            source_page=entity.source_page,
            modality=entity.modality,
            image_path=entity.image_path,
            caption=entity.caption,
            confidence=entity.confidence,
            metadata=entity.metadata,
        )

    # Relation
    def add_relation(self, relation: Relation):
        if relation.source not in self.entities:
            print(f"Skip source '{relation.source}'")
            return

        if relation.target not in self.entities:
            print(f"Skip target '{relation.target}'")
            return

        # Skip duplicate relation
        if self.has_relation(
            relation.source,
            relation.target,
            relation.relation,
        ):
            return

        # Add relation
        self.relations.append(relation)

        self.graph.add_edge(
            relation.source,
            relation.target,
            relation=relation.relation,
            description=relation.description,
            confidence=relation.confidence,
            source_page=relation.source_page,
            relation_obj=relation,
        )

    def has_relation(
        self,
        source: str,
        target: str,
        relation: str,
    ) -> bool:

        if not self.graph.has_edge(source, target):
            return False

        edge_dict = self.graph.get_edge_data(source, target)

        for _, data in edge_dict.items():
            if data.get("relation") == relation:
                return True

        return False

        # Getter
        def get_entity(self, entity_id):
            return self.entities.get(entity_id)

    # Statistics
    @property
    def num_entities(self):
        return len(self.entities)

    @property
    def num_relations(self):
        return len(self.relations)

    def statistics(self):
        return {
            "num_entities": self.num_entities,
            "num_relations": self.num_relations,
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
        }