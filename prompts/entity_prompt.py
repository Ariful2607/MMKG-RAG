ENTITY_PROMPT = """
You are an expert in Multimodal Knowledge Graph construction.

Extract every meaningful entity from the page.

For every entity return

- id
- name
- entity_type
- description

Return ONLY JSON.

Example

{
  "entities":[
    {
      "id":"E1",
      "name":"Transformer",
      "entity_type":"Model",
      "description":"Attention based neural network"
    }
  ]
}

Page:

{page}
"""