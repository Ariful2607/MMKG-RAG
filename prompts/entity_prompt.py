ENTITY_PROMPT = """
You are an expert in multimodal knowledge graphs.

Extract all entities from the following page.

For every entity return:

- id
- name
- type
- description

Return ONLY JSON.

Page:

{page}
"""