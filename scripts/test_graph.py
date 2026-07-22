from configs import load_config
from pipeline.graph_pipeline import GraphPipeline


def main():

    cfg = load_config()

    pipeline = GraphPipeline(cfg)

    graph = pipeline.build(
        "data/raw/sample.pdf"
    )

    print(graph.statistics())


if __name__ == "__main__":
    main()