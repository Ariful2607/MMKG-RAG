from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entity:
    id: str
    name: str
    entity_type: str
    description: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        return f"{self.name} ({self.entity_type})"