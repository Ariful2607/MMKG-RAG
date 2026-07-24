import json
from pathlib import Path

from omegaconf import OmegaConf

from graph.graph import KnowledgeGraph
from pipeline.graph_pipeline import GraphPipeline


def normalize(text):
    return text.lower().strip()


def keyword_score(prediction, ground_truth):
    gt = set(normalize(ground_truth).split())
    pred = set(normalize(prediction).split())

    if not gt:
        return 0.0

    return len(gt & pred) / len(gt)


def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():

    cfg = OmegaConf.load("configs/config.yaml")

    pipeline = GraphPipeline(cfg)

    graph = KnowledgeGraph.load("graph/megarag_graph.pkl")

    questions = json.load(
        open("evaluation/questions.json", encoding="utf-8")
    )

    results = []

    total_score = 0

    print_header("MegaRAG Evaluation")

    for sample in questions:

        question = sample["question"]
        gt = sample["ground_truth"]

        result = pipeline.answer(
            graph=graph,
            question=question,
        )

        prediction = result["answer"]

        score = keyword_score(prediction, gt)

        total_score += score

        print("-" * 70)
        print("Question:")
        print(question)

        print("\nPrediction:")
        print(prediction)

        print("\nGround Truth:")
        print(gt)

        print(f"\nKeyword Score: {score:.2f}")

        results.append({
            "question": question,
            "prediction": prediction,
            "ground_truth": gt,
            "keyword_score": score,
            "retrieval": result["retrieval"],
        })

    average = total_score / len(results)

    print_header("Summary")

    print(f"Average Keyword Score : {average:.3f}")

    Path("evaluation").mkdir(exist_ok=True)

    with open(
        "evaluation/results.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(results, f, indent=4)

    print("\nResults saved to evaluation/results.json")


if __name__ == "__main__":
    main()