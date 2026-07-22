from configs import load_config
from pipeline.graph_pipeline import GraphPipeline


def main():

    cfg = load_config()

    pipeline = GraphPipeline(cfg)

    graph = pipeline.build(
        "data/raw/sample.pdf"
    )

    print("\nGraph Statistics")
    print(graph.statistics())

    print("\n")

    question = "What is MegaRAG?"

    results = pipeline.retrieve(
        graph,
        question,
    )

    print("\nRetrieved Entities")

    for entity, score in results:

        print(
            f"{entity.name:40}"
            f"{score:.4f}"
        )

    results = pipeline.retrieve(
    graph,
    question,
)

    subgraph = pipeline.expand(
        graph,
        results,
        hops=2,
        max_neighbors=10,
    )

    print(subgraph.statistics())

if __name__ == "__main__":
    main()