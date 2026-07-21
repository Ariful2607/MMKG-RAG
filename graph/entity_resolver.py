import re

class EntityResolver:
    def __init__(self):
        pass

    def normalize(self, text: str):
        text = text.lower().strip()
        # remove multiple spaces
        text = " ".join(text.split())
        return text

    def remove_abbreviation(self, text: str):
        return re.sub(r"\s*\([^)]*\)", "", text).strip()

    def build_lookup(self, entities):
        lookup = {}
        for entity in entities:

            # original
            lookup[self.normalize(entity.name)] = entity

            # with abbreviation removed
            short = self.remove_abbreviation(entity.name)

            lookup[self.normalize(short)] = entity

        return lookup

    def resolve(self, name, lookup):
        key = self.normalize(name)
        return lookup.get(key)