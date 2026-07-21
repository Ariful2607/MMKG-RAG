ENTITY_PROMPT = """
You are an expert in scientific information extraction.

Extract the most important entities from the given scientific paper page.

Focus on entities that can later become nodes in a knowledge graph.

Prioritize:

- systems
- methods
- models
- algorithms
- frameworks
- datasets
- benchmarks
- tasks
- concepts
- modules
- components
- techniques

Do NOT extract:

- author names
- affiliations
- emails
- citations
- references
- page numbers
- copyright notices
- acknowledgements
- section numbers

Rules:

1. Extract between 5 and 10 entities.
2. Use the canonical entity name exactly as it appears in the paper.
3. Keep entity names concise.
4. Do NOT create IDs.
5. Do NOT invent entities that do not appear in the page.
6. Do NOT output duplicate entities.
7. Description should be one short sentence.

Return ONLY valid JSON.

{
  "entities": [
    {
      "name": "",
      "entity_type": "",
      "description": ""
    }
  ]
}
"""