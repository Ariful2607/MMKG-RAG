RELATION_PROMPT = """
You are constructing a scientific knowledge graph.

Your task is to extract relations ONLY between the provided entities.

You MUST NOT create new entities.

Both "source" and "target" MUST be copied EXACTLY from the Available Entities list.

If a name is not in the Available Entities list,
DO NOT use it.

Do NOT paraphrase entity names.

Do NOT shorten names.

Do NOT expand abbreviations.

If no valid relation exists, return [].

Only extract relations that are explicitly stated in the page.

Allowed relation types:

- uses
- extends
- builds_on
- improves
- supports
- evaluated_on
- contains
- part_of

Maximum 8 relations.

Return ONLY valid JSON.

[
    {
        "source":"",
        "target":"",
        "relation":"",
        "description":""
    }
]
"""