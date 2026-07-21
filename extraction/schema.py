from pydantic import BaseModel

class EntitySchema(BaseModel):
    id: str
    name: str
    entity_type: str
    description: str

class EntityListSchema(BaseModel):
    entities: list[EntitySchema]