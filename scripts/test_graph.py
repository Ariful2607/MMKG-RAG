from omegaconf import OmegaConf
from graph import graph
from graph.cross_page_linker import CrossPageLinker
from graph.embedding_generator import EmbeddingGenerator
from parser.pdf_parser import PDFParser
from models.factory import create_embedding, create_model
from extraction.entity_extractor import EntityExtractor
from extraction.relation_extractor import RelationExtractor
from graph.graph import KnowledgeGraph
from graph.graph_builder import GraphBuilder
from graph.duplicate_merger import DuplicateMerger

def main():

    cfg = OmegaConf.load("configs/default.yaml")

    # Load Model
    model = create_model(cfg)

    # Extractors
    entity_extractor = EntityExtractor(model)
    relation_extractor = RelationExtractor(model)

    # Graph
    graph = KnowledgeGraph()

    # Graph Builder
    builder = GraphBuilder(
        entity_extractor=entity_extractor,
        relation_extractor=relation_extractor,
        graph=graph,
        cfg=cfg,
    )

    # Parse PDF
    parser = PDFParser("data/raw/sample.pdf")
    document = parser.parse()

    # Build Graph
    builder.process_document(document)

    merger = DuplicateMerger()
    merger.merge(graph)

    # Generate Embeddings
    embedding_model = create_embedding(cfg)
    generator = EmbeddingGenerator(embedding_model)
    generator.generate(graph)

    # Cross Page Linking
    linker = CrossPageLinker(
        threshold=0.90
    )
    linker.link(graph)

    # Statistics
    print("\n========== Graph Statistics ==========")
    print(graph.statistics())


if __name__ == "__main__":
    main()