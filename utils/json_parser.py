import json
import re

def extract_json(text):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL,
    )

    if match is None:
        raise ValueError("JSON not found")

    return json.loads(match.group())