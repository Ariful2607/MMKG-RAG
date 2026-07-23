class ResearchLogger:
    @staticmethod
    def print_retrieval(results):
        print("=" * 70)
        print("Top-k Retrieval")
        print("=" * 70)

        print(f"{'Rank':<5}{'Entity':<45}{'Score'}")

        for i, item in enumerate(results, 1):

            print(
                f"{i:<5}"
                f"{item['entity']:<45}"
                f"{item['score']:.4f}"
            )