import json

from graph.entity import Entity
from extraction.schema import EntityListSchema
from prompts.entity_prompt import ENTITY_PROMPT

from utils.json_parser import extract_json

class EntityExtractor:
    def __init__(self, llm):
        self.llm = llm
    def extract(self, page):
        prompt = ENTITY_PROMPT.format(
            page=page.text
        )
        response = model.generate(
        image=page.image_path,
        text=page.text,
        prompt=ENTITY_PROMPT,
    )

    data = extract_json(response.text)
        # response = self.llm.generate(prompt)
        # from extraction.parser import extract_json
        # data = extract_json(
        #     response.text
        # )

        result = EntityListSchema.model_validate(data)
        entities = []

        for item in result.entities:
            entities.append(
                Entity(
                    id=item.id,
                    name=item.name,
                    entity_type=item.entity_type,
                    description=item.description,
                )
            )
        return entities