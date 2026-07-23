RELATION_PROMPT = """
You are constructing a scientific Knowledge Graph.

Your task is to extract relations ONLY between the provided entities.

IMPORTANT:

- NEVER create new entities.
- Both "source" and "target" MUST be copied EXACTLY from the Available Entities list.
- If an entity is not listed, DO NOT use it.
- Do NOT paraphrase entity names.
- Do NOT shorten names.
- Do NOT expand abbreviations.

Only extract relations that are explicitly stated in the page.

Do NOT infer relations using outside knowledge.

If no valid relation exists, return [].

Allowed relation types:

- uses
- extends
- builds_on
- improves
- supports
- evaluated_on
- trained_on
- compared_with
- contains
- consists_of
- integrates
- aligns_with
- retrieves
- generates
- part_of

Rules:

1. Extract only explicit relations.
2. Do NOT guess.
3. Description should briefly explain the relation.
4. Avoid duplicate relations.
5. If multiple relation types are possible, choose the most specific one.

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