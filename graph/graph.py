import networkx as nx

from graph.entity import Entity
from graph.relation import Relation


class KnowledgeGraph:
    def __init__(self):
        self.entities = {}
        self.relations = []
        self.graph = nx.MultiDiGraph()
    
    def add_entity(self, entity):
        if entity.id in self.entities:
            return
        self.entities[entity.id] = entity
        self.graph.add_node(
            entity.id,
            **entity.__dict__,
        )
    
    def add_relation(self, relation):
        self.relations.append(relation)
        self.graph.add_edge(
            relation.head,
            relation.tail,
            relation=relation.relation,
            confidence=relation.confidence,
            source=relation.source,
        )

    @property
    def num_entities(self):
        return self.graph.number_of_nodes()

    @property
    def num_relations(self):
        return self.graph.number_of_edges()
    
    def statistics(self):
        return {
            "num_entities": len(self.entities),
            "num_relations": len(self.relations),
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
    }