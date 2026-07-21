from omegaconf import OmegaConf
from parser.pdf_parser import PDFParser
from models.factory import create_model
from extraction.entity_extractor import EntityExtractor
from graph.graph import KnowledgeGraph
from graph.graph_builder import GraphBuilder

def main():
    cfg = OmegaConf.load("configs/default.yaml")
    model = create_model(cfg)
    extractor = EntityExtractor(model)
    graph = KnowledgeGraph()
    builder = GraphBuilder(
        extractor=extractor,
        graph=graph,
        cfg=cfg,
    )
    parser = PDFParser("data/raw/sample.pdf")
    document = parser.parse()
    builder.process_document(document)
    stats = graph.statistics()
    print(stats)

if __name__ == "__main__":
    main()