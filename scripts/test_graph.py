from configs import load_config
from pipeline.graph_pipeline import GraphPipeline


def main():

    cfg = load_config()

    pipeline = GraphPipeline(cfg)

    graph = pipeline.build(
        "data/raw/sample.pdf"
    )

    print(graph.statistics())

    question = "What is MegaRAG?"

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

    context = pipeline.build_context(
        subgraph,
    )

    print(context)

    answer = pipeline.answer(
        graph,
        question,
    )

    print(answer)

if __name__ == "__main__":
    main()