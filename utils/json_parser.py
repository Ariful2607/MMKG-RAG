import json

def extract_json(text: str):
    decoder = json.JSONDecoder()
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON found.")
    obj, _ = decoder.raw_decode(text[start:])
    return obj