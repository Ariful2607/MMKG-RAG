from graph.relation import Relation
from prompts.relation_prompt import RELATION_PROMPT
from utils.json_parser import extract_json

class RelationExtractor:

    def __init__(self, model):
        self.model = model

    def extract(self, page, entities):
        if len(entities) < 2:
            return []

        entity_text = "\n".join(
            f"- {e.name} ({e.entity_type})"
            for e in entities
        )

        prompt = (
            RELATION_PROMPT
            + "\n\nAvailable Entities:\n"
            + entity_text
        )

        response = self.model.generate(
            image=page.image_path,
            text=page.text,
            prompt=prompt,
        )

        print(response.text)

        data = extract_json(response.text)

        if isinstance(data, dict):
            data = data.get("relations", [])

        relations = []

        for item in data:

            source = item.get("source", "").strip()
            target = item.get("target", "").strip()
            relation = item.get("relation", "").strip()

            if not source or not target or not relation:
                continue

            relations.append(
                Relation(
                    source=source,
                    target=target,
                    relation=relation,
                    description=item.get("description", "").strip(),
                    confidence=1.0,
                    source_page=page.page_number,
                )
            )

        return relations