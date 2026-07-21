import networkx as nx
from graph.entity import Entity
from graph.relation import Relation


class KnowledgeGraph:
    def __init__(self):
        self.entities = {}
        self.relations = []
        self.graph = nx.MultiDiGraph()

    def add_entity(self, entity: Entity):
        if entity.id in self.entities:
            return
        self.entities[entity.id] = entity
        self.graph.add_node(
            entity.id,
            **entity.__dict__,
        )

    def add_relation(self, relation: Relation):
        if relation.source not in self.graph:
            return
        if relation.target not in self.graph:
            return

        self.relations.append(relation)
        self.graph.add_edge(
            relation.source,
            relation.target,
            relation=relation.relation,
            confidence=relation.confidence,
            source=relation.source,
            description=relation.description,
        )

    def get_entity(self, entity_id):
        return self.entities.get(entity_id)

    @property
    def num_entities(self):
        return self.graph.number_of_nodes()

    @property
    def num_relations(self):
        return self.graph.number_of_edges()

    def statistics(self):
        return {
            "num_entities": self.num_entities,
            "num_relations": self.num_relations,
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
        }