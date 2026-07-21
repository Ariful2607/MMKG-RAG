import json
import re

def extract_json(text: str):
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found.")
    decoder = json.JSONDecoder()
    obj, end = decoder.raw_decode(text[start:])
    return obj
