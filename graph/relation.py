from dataclasses import dataclass


@dataclass
class Relation:
    source: str
    target: str
    relation: str
    confidence: float = 1.0

    def __str__(self):
        return f"{self.source} --{self.relation}--> {self.target}"