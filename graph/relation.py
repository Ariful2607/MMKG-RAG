from dataclasses import dataclass

@dataclass
class Relation:
    source: str
    target: str
    relation: str
    description: str = ""
    confidence: float = 1.0
    source_page: int = 0