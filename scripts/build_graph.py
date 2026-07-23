from pathlib import Path
from omegaconf import OmegaConf
from pipeline.graph_pipeline import GraphPipeline


def main():
    cfg = OmegaConf.load("configs/config.yaml")
    pipeline = GraphPipeline(cfg)
    pdf_path = "data/raw/sample.pdf"
    graph = pipeline.build(pdf_path)
    Path("graphs").mkdir(exist_ok=True)
    save_path = "graph/megarag_graph.pkl"
    graph.save(save_path)
    print()
    print("=" * 70)
    print("GRAPH SAVED")
    print("=" * 70)
    print(save_path)
    print()
    print(graph.statistics())


if __name__ == "__main__":
    main()