import json
import re

def extract_json(text: str):
    text = re.sub(
        r"```json",
        "",
        text,
    )

    text = re.sub(
        r"```",
        "",
        text,
    )

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("JSON not found")
    return json.loads(
        text[start:end+1]
    )