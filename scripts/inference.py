from omegaconf import OmegaConf
from pipeline.graph_pipeline import GraphPipeline

cfg = OmegaConf.load("configs/config.yaml")
pipeline = GraphPipeline(cfg)
graph = pipeline.build("data/raw/sample.pdf")
question = "What is MegaRAG?"
result = pipeline.answer(
    graph=graph,
    question=question,
)

print("\n" + "=" * 70)
print("QUESTION")
print("=" * 70)
print(question)

print("\n" + "=" * 70)
print("TOP-K RETRIEVAL")
print("=" * 70)

for i, item in enumerate(result["retrieval"], start=1):
    print(
        f"{i:>2}. "
        f"{item['entity']:<45}"
        f"score={item['score']:.4f}"
    )

print("\n" + "=" * 70)
print("EXPANDED SUBGRAPH")
print("=" * 70)

print(f"Nodes     : {len(graph.entities)}")
print(f"Relations : {len(graph.relations)}")

print("\n" + "=" * 70)
print("LLM CONTEXT")
print("=" * 70)

print(result["context"])

print("\n" + "=" * 70)
print("GENERATED ANSWER")
print("=" * 70)

print(result["answer"])