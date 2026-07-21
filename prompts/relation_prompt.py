RELATION_PROMPT = """
You are an expert in scientific knowledge graph construction.

Given a scientific paper page and the extracted entities,
identify semantic relationships between them.

Return ONLY JSON.

[
    {
        "source":"MegaRAG",
        "target":"Knowledge Graphs",
        "relation":"uses",
        "description":"MegaRAG utilizes Knowledge Graphs."
    }
]

Possible relations include:

uses
extends
contains
improves
built_on
evaluates_on
trained_on
compares_with
supports
consists_of
retrieves_from
reasons_over

Return between 3 and 15 relations.
"""