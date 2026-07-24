import json
from json_repair import repair_json


def load_llm_json(text):
    try:
        return json.loads(text)

    except json.JSONDecodeError:
        repaired = repair_json(text)
        return json.loads(repaired)