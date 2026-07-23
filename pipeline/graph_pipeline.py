from parser.pdf_parser import PDFParser

from extraction.entity_extractor import EntityExtractor
from extraction.relation_extractor import RelationExtractor

from graph.cross_page_linker import CrossPageLinker
from graph.duplicate_merger import DuplicateMerger
from graph.embedding_generator import EmbeddingGenerator
from graph.graph import KnowledgeGraph
from graph.graph_builder import GraphBuilder
from graph.graph_retriever import GraphRetriever
from graph.neighbor_expander import NeighborExpander

from models.embedding import EmbeddingModel
from models.qwen_llm import QwenLLM
from models.qwen_vl import QwenVLModel

from pipeline.context_builder import ContextBuilder
from pipeline.generator import Generator


class GraphPipeline:
    """End-to-end MegaRAG graph construction, retrieval, and generation pipeline."""

    def __init__(self, cfg):
        self.cfg = cfg

        print("=" * 70)
        print("Initializing Models...")
        print("=" * 70)

        # Models
        self.vlm = QwenVLModel(cfg)
        self.embedding_model = EmbeddingModel(cfg)
        self.llm = QwenLLM(cfg)

        # Extraction
        self.entity_extractor = EntityExtractor(self.vlm)
        self.relation_extractor = RelationExtractor(self.vlm)

        # Retrieval and generation
        self.retriever = GraphRetriever(self.embedding_model)
        self.expander = NeighborExpander()
        self.context_builder = ContextBuilder()
        self.generator = Generator(self.llm)

    def build(self, pdf_path):
        """Build and enrich a knowledge graph from a PDF document."""
        print("\n" + "=" * 70)
        print("Building Knowledge Graph")
        print("=" * 70)

        parser = PDFParser(pdf_path)
        document = parser.parse()

        graph = KnowledgeGraph()

        graph_builder = GraphBuilder(
            entity_extractor=self.entity_extractor,
            relation_extractor=self.relation_extractor,
            graph=graph,
            cfg=self.cfg,
        )

        graph = graph_builder.process_document(document)

        print("\n========== Duplicate Merge ==========")
        DuplicateMerger().merge(graph)

        EmbeddingGenerator(self.embedding_model).generate(graph)

        graph_config = self.cfg.get("graph", {})
        similarity_threshold = graph_config.get(
            "cross_page_similarity",
            0.90,
        )

        CrossPageLinker(
            threshold=similarity_threshold
        ).link(graph)

        print("\n========== Final Graph ==========")
        print(graph.statistics())

        return graph

    def retrieve(self, graph, question, top_k=None):
        """Retrieve the most semantically relevant graph entities."""
        if top_k is None:
            top_k = self.cfg.retrieval.get("top_k", 5)

        return self.retriever.retrieve(
            graph=graph,
            question=question,
            top_k=top_k,
        )

    def expand(
        self,
        graph,
        retrieval_results,
        hops=None,
        max_neighbors=None,
    ):
        """Expand retrieved entities into a k-hop evidence subgraph."""
        if hops is None:
            hops = self.cfg.retrieval.get("hops", 1)

        if max_neighbors is None:
            max_neighbors = self.cfg.retrieval.get(
                "max_neighbors",
                None,
            )

        return self.expander.expand(
            graph=graph,
            retrieval_results=retrieval_results,
            hops=hops,
            max_neighbors=max_neighbors,
        )

    def build_context(self, subgraph):
        """Serialize a retrieved subgraph into LLM-readable context."""
        return self.context_builder.build(subgraph)

    def answer(
        self,
        graph,
        question,
        top_k=None,
        hops=None,
        max_neighbors=None,
    ):
        """
        Answer a question using graph retrieval, expansion, context building,
        and local Qwen text generation.
        """
        retrieval_results = self.retrieve(
            graph=graph,
            question=question,
            top_k=top_k,
        )

        subgraph = self.expand(
            graph=graph,
            retrieval_results=retrieval_results,
            hops=hops,
            max_neighbors=max_neighbors,
        )

        context = self.build_context(subgraph)

        response = self.generator.generate(
            question=question,
            context=context,
        )

        return {
            "answer": response.text,
            "context": context,
            "retrieval": [
                {
                    "entity": entity.name,
                    "score": round(float(score), 4),
                }
                for entity, score in retrieval_results
            ],
            "subgraph": {
                "num_entities": len(subgraph.entities),
                "num_relations": len(subgraph.relations),
                "entities": [
                    entity.name
                    for entity in subgraph.entities.values()
                ],
            },
        }