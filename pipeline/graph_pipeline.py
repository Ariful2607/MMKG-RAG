from parser.pdf_parser import PDFParser

from graph.graph import KnowledgeGraph
from graph.graph_builder import GraphBuilder
from graph.duplicate_merger import DuplicateMerger
from graph.embedding_generator import EmbeddingGenerator
from graph.cross_page_linker import CrossPageLinker

from extraction.entity_extractor import EntityExtractor
from extraction.relation_extractor import RelationExtractor

from models.qwen_vl import QwenVLModel
from models.embedding import EmbeddingModel


class GraphPipeline:

    def __init__(self, cfg):

        self.cfg = cfg

        print("=" * 70)
        print("Initializing Models...")
        print("=" * 70)

        # ----------------------------
        # Models
        # ----------------------------

        self.vlm = QwenVLModel(cfg)
        self.embedding_model = EmbeddingModel(cfg)

        # ----------------------------
        # Extractors
        # ----------------------------

        self.entity_extractor = EntityExtractor(self.vlm)
        self.relation_extractor = RelationExtractor(self.vlm)

    def build(self, pdf_path):

        print("\n" + "=" * 70)
        print("Building Knowledge Graph")
        print("=" * 70)

        # ----------------------------
        # Parse PDF
        # ----------------------------

        parser = PDFParser(pdf_path)

        document = parser.parse()

        # ----------------------------
        # Empty Graph
        # ----------------------------

        graph = KnowledgeGraph()

        # ----------------------------
        # Build Graph
        # ----------------------------

        builder = GraphBuilder(
            entity_extractor=self.entity_extractor,
            relation_extractor=self.relation_extractor,
            graph=graph,
            cfg=self.cfg,
        )

        graph = builder.process_document(document)

        # ----------------------------
        # Duplicate Merge
        # ----------------------------

        print("\n========== Duplicate Merge ==========")

        DuplicateMerger().merge(graph)

        # ----------------------------
        # Generate Embeddings
        # ----------------------------

        EmbeddingGenerator(
            self.embedding_model
        ).generate(graph)

        # ----------------------------
        # Cross-page Linking
        # ----------------------------

        CrossPageLinker(
            threshold=self.cfg.graph.cross_page_similarity
        ).link(graph)

        print("\n========== Final Graph ==========")

        stats = graph.statistics()

        print(stats)

        return graph