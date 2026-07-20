from graph.entity import Entity
from graph.relation import Relation
from graph.graph import KnowledgeGraph

kg = KnowledgeGraph()

kg.add_entity(
    Entity(
        id="E1",
        name="Transformer",
        entity_type="Model",
    )
)

kg.add_entity(
    Entity(
        id="E2",
        name="Attention",
        entity_type="Concept",
    )
)

kg.add_relation(
    Relation(
        source="E1",
        target="E2",
        relation="uses",
    )
)

print("Entities :", kg.num_entities)
print("Relations:", kg.num_relations)