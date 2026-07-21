from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker

class GraphBuilder:
    def __init__(self, extractor, graph, cfg):
        self.extractor = extractor
        self.graph = graph
        self.cfg = cfg
        self.chunker = TextChunker(
            cfg.preprocessing.chunk_size,
            cfg.preprocessing.overlap,
        )

    def process_page(self, page):
        text = TextCleaner.clean(page.text)
        chunks = self.chunker.split(text)
        if self.cfg.debug.enabled:
            chunks = chunks[:self.cfg.debug.max_chunks_per_page]
        total_entities = 0
        for i, chunk in enumerate(chunks, start=1):
            # gunakan chunk ini sebagai input
            page.text = chunk
            print(f"\nChunk {i}/{len(chunks)}")
            entities = self.extractor.extract(page)
            print(f"Extracted {len(entities)} entities")
            for entity in entities:
                print(f"  - {entity.name} ({entity.entity_type})")
                self.graph.add_entity(entity)
            total_entities += len(entities)
        print(f"Total entities on page {page.page_number}: {total_entities}")

    def process_document(self, document):
        pages = document.pages
        if self.cfg.debug.enabled:
            pages = pages[:self.cfg.debug.max_pages]
        for page in pages:
            print(f"\n========== Processing Page {page.page_number} ==========")
            self.process_page(page)