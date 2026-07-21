from pydantic import BaseModel, Field

class EntitySchema(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    entity_type: str = Field(...)
    description: str = Field(default="")

class EntityListSchema(BaseModel):
    entities: list[EntitySchema]