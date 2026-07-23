from omegaconf import OmegaConf
from graph.graph import KnowledgeGraph
from pipeline.graph_pipeline import GraphPipeline

def print_header(title):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    cfg = OmegaConf.load("configs/config.yaml")
    pipeline = GraphPipeline(cfg)
    print_header("Loading Knowledge Graph")
    graph = KnowledgeGraph.load("graph/megarag_graph.pkl")
    print(graph.statistics())
    while True:
        question = input("\nQuestion (type 'exit' to quit): ")
        if question.lower() == "exit":
            break

        result = pipeline.answer(
            graph=graph,
            question=question,
        )

        print_header("Top-k Retrieval")

        for i, item in enumerate(result["retrieval"], 1):
            print(
                f"{i:>2}. "
                f"{item['entity']:<50}"
                f"{item['score']:.4f}"
            )

        print_header("Subgraph")
        print(
            f"Entities : {result['subgraph']['num_entities']}"
        )

        print(
            f"Relations: {result['subgraph']['num_relations']}"
        )

        print("\nEntities")
        for entity in result["subgraph"]["entities"]:

            print(f" • {entity}")
        print_header("Generated Answer")
        print(result["answer"])

if __name__ == "__main__":
    main()