from graph.entity import Entity
from extraction.schema import EntityListSchema
from utils.json_parser import extract_json
from prompts.entity_prompt import ENTITY_PROMPT

class EntityExtractor:
    def __init__(self, model):
        self.model = model
    
    def extract(self, page):

        response = self.model.generate(
            image=page.image_path,
            text=page.text,
            prompt=ENTITY_PROMPT,
        )

        try:
            data = extract_json(response.text)
            schema = EntityListSchema(**data)

        except Exception as e:
            print("Entity extraction failed:", e)
            return []

        entities = []

        for e in schema.entities:
            entities.append(
                Entity(
                    id=e.id,
                    name=e.name,
                    entity_type=e.entity_type,
                    description=e.description,
                    source_page=page.page_number,
                )
            )

        return entities