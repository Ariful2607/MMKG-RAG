ENTITY_PROMPT = """
You are an expert in scientific information extraction.

Your task is to construct a high-quality scientific knowledge graph from an academic paper.

Extract the most important entities from the given page.

The extracted entities will later become nodes in a Knowledge Graph for Retrieval-Augmented Generation (RAG).

Prioritize entities such as:

- Methods
- Models
- Frameworks
- Algorithms
- Datasets
- Benchmarks
- Tasks
- Concepts
- Components
- Modules
- Techniques
- Metrics
- Loss Functions

Do NOT extract:

- Author names
- Affiliations
- Emails
- Citations
- References
- Page numbers
- Figure numbers
- Table numbers
- Copyright notices
- Acknowledgements
- Section numbers

Rules:

1. Extract ALL important entities from the page.
2. Use the canonical entity name exactly as it appears in the paper.
3. Keep entity names concise.
4. Do NOT create IDs.
5. Do NOT invent entities.
6. Do NOT output duplicate entities.
7. If an entity appears multiple times, extract it only once.
8. If a compound phrase represents one concept, keep it as one entity.
9. Description should be one short sentence describing the entity.

Allowed entity types:

- Method
- Model
- Framework
- Algorithm
- Dataset
- Benchmark
- Task
- Concept
- Component
- Module
- Technique
- Metric
- Loss Function

Return ONLY valid JSON.

{
    "entities":[
        {
            "name":"",
            "entity_type":"",
            "description":""
        }
    ]
}
"""