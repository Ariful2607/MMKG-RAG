from dataclasses import dataclass, field
from pathlib import Path
from parser.page import Page
from graph.graph import KnowledgeGraph

@dataclass
class Document:
    name: str
    path: Path
    pages: list[Page] = field(default_factory=list)
    graph: KnowledgeGraph | None = None

    @property
    def num_pages(self):
        return len(self.pages)

    def add_page(self, page: Page):
        self.pages.append(page)