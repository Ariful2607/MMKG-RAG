from copy import copy

from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker


class GraphBuilder:

    def __init__(
        self,
        entity_extractor,
        relation_extractor,
        graph,
        cfg,
    ):

        self.entity_extractor = entity_extractor
        self.relation_extractor = relation_extractor
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
            chunks = chunks[: self.cfg.debug.max_chunks_per_page]

        total_entities = 0
        total_relations = 0

        for idx, chunk in enumerate(chunks, start=1):

            print(f"\n========== Chunk {idx}/{len(chunks)} ==========")

            # jangan ubah page asli
            chunk_page = copy(page)
            chunk_page.text = chunk

            ##################################################
            # Entity Extraction
            ##################################################

            entities = self.entity_extractor.extract(chunk_page)

            print(f"Extracted {len(entities)} entities")

            entity_lookup = {}

            for entity in entities:

                print(
                    f"  • {entity.name} ({entity.entity_type})"
                )

                self.graph.add_entity(entity)

                entity_lookup[entity.name.lower()] = entity

            ##################################################
            # Relation Extraction
            ##################################################

            relations = self.relation_extractor.extract(
                chunk_page,
                entities,
            )

            print(f"Extracted {len(relations)} relations")

            for relation in relations:

                source = entity_lookup.get(
                    relation.source.lower()
                )

                target = entity_lookup.get(
                    relation.target.lower()
                )

                if source is None:

                    print(
                        f"  Skip: source entity "
                        f"'{relation.source}' not found."
                    )

                    continue

                if target is None:

                    print(
                        f"  Skip: target entity "
                        f"'{relation.target}' not found."
                    )

                    continue

                print(
                    f"  • {relation.source}"
                    f" --{relation.relation}--> "
                    f"{relation.target}"
                )

                self.graph.add_relation(relation)

            total_entities += len(entities)
            total_relations += len(relations)

        print(
            f"\nPage {page.page_number} Summary"
        )
        print(f"Entities : {total_entities}")
        print(f"Relations: {total_relations}")

    def process_document(self, document):

        pages = document.pages

        if self.cfg.debug.enabled:
            pages = pages[: self.cfg.debug.max_pages]

        print(f"\nProcessing {len(pages)} pages...\n")

        for page in pages:

            print("=" * 60)
            print(f"Processing Page {page.page_number}")
            print("=" * 60)

            self.process_page(page)

        print("\n========== Graph Statistics ==========")

        stats = self.graph.statistics()

        print(f"Entities : {stats['num_entities']}")
        print(f"Relations: {stats['num_relations']}")
        print(f"Nodes    : {stats['num_nodes']}")
        print(f"Edges    : {stats['num_edges']}")

        return self.graph