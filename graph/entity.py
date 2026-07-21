from dataclasses import dataclass, field
from typing import Any

@dataclass
class Entity:
    id: str
    name: str
    entity_type: str
    description: str = ""
    source_page: int = -1
    modality: str = "text"
    image_path: str | None = None
    caption: str | None = None
    confidence: float = 1.0
    metadata: dict = field(default_factory=dict)

    def __str__(self):
        return f"{self.name} ({self.entity_type})"