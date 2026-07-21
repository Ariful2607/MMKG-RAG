ENTITY_PROMPT = """
You are an expert in scientific information extraction.

Extract the most important TECHNICAL entities from this scientific paper.

Prioritize:

- methods
- models
- algorithms
- datasets
- benchmarks
- tasks
- frameworks
- systems
- metrics
- concepts

Ignore:

- author names
- affiliations
- emails
- page numbers
- copyright
- references
- acknowledgements

Return between 5 and 10 entities.

Return ONLY valid JSON.

{
  "entities":[
    {
      "id":"",
      "name":"",
      "entity_type":"",
      "description":""
    }
  ]
}
"""