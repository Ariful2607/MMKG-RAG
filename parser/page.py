from dataclasses import dataclass
from pathlib import Path

@dataclass
class Page:
    page_number: int
    text: str
    image_path: Path