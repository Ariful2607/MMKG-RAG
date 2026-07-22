from parser.pdf_parser import PDFParser

from graph.graph import KnowledgeGraph
from graph.graph_builder import GraphBuilder
from graph.duplicate_merger import DuplicateMerger
from graph.embedding_generator import EmbeddingGenerator
from graph.cross_page_linker import CrossPageLinker
from graph.graph_retriever import GraphRetriever
from graph.neighbor_expander import NeighborExpander


from extraction.entity_extractor import EntityExtractor
from extraction.relation_extractor import RelationExtractor
from pipeline.context_builder import ContextBuilder

from models.qwen_vl import QwenVLModel
from models.embedding import EmbeddingModel


class GraphPipeline:

    def __init__(self, cfg):

        self.cfg = cfg

        print("=" * 70)
        print("Initializing Models...")
        print("=" * 70)

        self.vlm = QwenVLModel(cfg)
        self.embedding_model = EmbeddingModel(cfg)

        self.entity_extractor = EntityExtractor(self.vlm)
        self.relation_extractor = RelationExtractor(self.vlm)

        self.retriever = GraphRetriever(self.embedding_model)

        self.expander = NeighborExpander()
        self.context_builder = ContextBuilder()

    ####################################################
    # Build Graph
    ####################################################

    def build(self, pdf_path):

        print("\n" + "=" * 70)
        print("Building Knowledge Graph")
        print("=" * 70)

        parser = PDFParser(pdf_path)

        document = parser.parse()

        graph = KnowledgeGraph()

        builder = GraphBuilder(
            entity_extractor=self.entity_extractor,
            relation_extractor=self.relation_extractor,
            graph=graph,
            cfg=self.cfg,
        )

        graph = builder.process_document(document)

        DuplicateMerger().merge(graph)

        EmbeddingGenerator(
            self.embedding_model
        ).generate(graph)

        CrossPageLinker(
            threshold=self.cfg.graph.cross_page_similarity
        ).link(graph)

        return graph

    ####################################################
    # Retrieve
    ####################################################

    def retrieve(
        self,
        graph,
        question,
        top_k=None,
    ):

        if top_k is None:
            top_k = self.cfg.retrieval.top_k

        return self.retriever.retrieve(
            graph,
            question,
            top_k,
        )
    #####################################################
    # Expand
    #####################################################
    
    def expand(
        self,
        graph,
        retrieval_results,
        hops=1,
        max_neighbors=None,
    ):
        return self.expander.expand(
            graph=graph,
            retrieval_results=retrieval_results,
            hops=hops,
            max_neighbors=max_neighbors,
        )
    
    ####################################################
    # Build Context
    ####################################################
    
    def build_context(
        self,
        subgraph,
    ):

        return self.context_builder.build(
            subgraph,
        )