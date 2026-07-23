import json
import re

def extract_json(text: str):
    """
    Extract JSON object or array from LLM output.
    Supports:
        - {...}
        - [...]
        - ```json ... ```
    """

    # Remove markdown fences
    text = re.sub(r"^```json\s*", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    text = text.strip()

    decoder = json.JSONDecoder()

    # Find the first JSON structure
    obj_start = text.find("{")
    arr_start = text.find("[")

    if obj_start == -1 and arr_start == -1:
        raise ValueError("No JSON found.")

    # Choose whichever comes first
    if obj_start == -1:
        start = arr_start
    elif arr_start == -1:
        start = obj_start
    else:
        start = min(obj_start, arr_start)

    data, _ = decoder.raw_decode(text[start:])

    return data