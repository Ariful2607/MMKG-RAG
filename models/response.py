from dataclasses import dataclass

@dataclass
class ModelResponse:
    text: str
    raw: object = None