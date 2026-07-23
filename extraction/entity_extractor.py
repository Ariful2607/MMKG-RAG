from graph.entity import Entity
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
        print("=" * 80)
        print(response.text)
        print("=" * 80)

        try:
            data = extract_json(response.text)
            print(data)
            # Normalize LLM output
            if isinstance(data, dict):
                if "entities" in data:
                    entities_data = data["entities"]

                elif "name" in data:
                    entities_data = [data]

                else:
                    entities_data = []

            elif isinstance(data, list):
                entities_data = data

            else:
                entities_data = []

        except Exception as e:
            print("Entity extraction failed:", e)
            return []

        # Build Entity Objects
        entities = []

        for idx, item in enumerate(entities_data):
            entity = Entity(
                id=f"p{page.page_number}_e{idx}",
                name=item.get("name", "").strip(),
                entity_type=item.get("entity_type", "").strip(),
                description=item.get("description", "").strip(),
                source_page=page.page_number,
            )
            entities.append(entity)
        return entities