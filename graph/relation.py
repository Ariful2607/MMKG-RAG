from dataclasses import dataclass

@dataclass
class Relation:
    head: str
    relation: str
    tail: str
    confidence: float = 1.0
    source_page: int = -1
    source: str = "vlm"

    def __str__(self):
        return f"{self.source} --{self.relation}--> {self.target}"