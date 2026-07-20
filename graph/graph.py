import networkx as nx

from graph.entity import Entity
from graph.relation import Relation


class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
    
    def add_entity(self, entity: Entity):
        self.graph.add_node(
            entity.id,
            name=entity.name,
            entity_type=entity.entity_type,
            description=entity.description,
            attributes=entity.attributes,
        )
    
    def add_relation(self, relation: Relation):
        self.graph.add_edge(
            relation.source,
            relation.target,
            relation=relation.relation,
            confidence=relation.confidence,
        )

    @property
    def num_entities(self):
        return self.graph.number_of_nodes()

    @property
    def num_relations(self):
        return self.graph.number_of_edges()