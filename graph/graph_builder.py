from copy import copy

from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker
from graph.entity_resolver import EntityResolver
from graph.relation import Relation


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

        self.resolver = EntityResolver()

        self.chunker = TextChunker(
            cfg.preprocessing.chunk_size,
            cfg.preprocessing.overlap,
        )

    ##################################################
    # Process One Page
    ##################################################

    def process_page(self, page):

        text = TextCleaner.clean(page.text)
        chunks = self.chunker.split(text)

        if self.cfg.debug.enabled:
            chunks = chunks[: self.cfg.debug.max_chunks_per_page]

        total_entities = 0
        total_relations = 0

        for idx, chunk in enumerate(chunks, start=1):

            print(f"\n========== Chunk {idx}/{len(chunks)} ==========")

            chunk_page = copy(page)
            chunk_page.text = chunk

            ##################################################
            # Entity Extraction
            ##################################################

            entities = self.entity_extractor.extract(chunk_page)

            print(f"Extracted {len(entities)} entities")

            for entity in entities:
                self.graph.add_entity(entity)

            entity_lookup = self.resolver.build_lookup(
                entities
            )

            ##################################################
            # Relation Extraction
            ##################################################

            relations = self.relation_extractor.extract(
                chunk_page,
                entities,
            )

            print(f"Extracted {len(relations)} relations")

            added_relations = 0

            for relation in relations:

                source_entity = self.resolver.resolve(
                    relation.source,
                    entity_lookup,
                )

                target_entity = self.resolver.resolve(
                    relation.target,
                    entity_lookup,
                )

                ##################################################
                # Skip missing entity
                ##################################################

                if source_entity is None:

                    print(
                        f"  Skip: source entity "
                        f"'{relation.source}' not found."
                    )

                    continue

                if target_entity is None:

                    print(
                        f"  Skip: target entity "
                        f"'{relation.target}' not found."
                    )

                    continue

                ##################################################
                # Debug
                ##################################################

                print(
                    f"  • {source_entity.name}"
                    f" --{relation.relation}--> "
                    f"{target_entity.name}"
                )

                ##################################################
                # Convert Name -> Internal ID
                ##################################################

                graph_relation = Relation(
                    source=source_entity.id,
                    target=target_entity.id,
                    relation=relation.relation,
                    description=relation.description,
                    confidence=relation.confidence,
                    source_page=relation.source_page,
                )

                self.graph.add_relation(graph_relation)

                added_relations += 1

            total_entities += len(entities)
            total_relations += added_relations

        ##################################################
        # Page Summary
        ##################################################

        print(f"\nPage {page.page_number} Summary")

        print(f"Entities : {total_entities}")

        print(f"Relations: {total_relations}")

    ##################################################
    # Process Whole Document
    ##################################################

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

        ##################################################
        # Graph Statistics
        ##################################################

        print("\n========== Graph Statistics ==========")

        stats = self.graph.statistics()

        print(f"Entities : {stats['num_entities']}")
        print(f"Relations: {stats['num_relations']}")
        print(f"Nodes    : {stats['num_nodes']}")
        print(f"Edges    : {stats['num_edges']}")

        return self.graph