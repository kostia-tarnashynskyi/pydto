from pydantic import BaseModel, Field
from pydto.pydantic_v2 import dto


def test_dto_pydantic_v2():
    class BaseEntityExample(BaseModel):
        id: str = Field(...)
        name: str = Field(...)
        description: str | None = None

        class Config:
            from_attributes = True

        def get_projection_fields(self) -> list[str]:
            return list(self.model_fields.keys())

    @dto(
        partial=True,
        pick_fields=["id", "name", "description"],
        omit_fields=[],
        rename_fields={},
        config={
            "from_attributes": False,
            "json_schema_extra": {
                "example": {
                    "id": "entity_123",
                    "name": "Sample Entity",
                    "description": "This is a sample entity for demonstration purposes.",
                }
            },
        },
    )
    class PartialEntity(BaseEntityExample):
        ...

    # Create an instance of PartialEntity
    entity = PartialEntity(id="entity_123", name="Sample Entity", description="Demo")

    # Print the instance
    print(entity)

    # Assert field values
    assert entity.id == "entity_123"
    assert entity.name == "Sample Entity"
    assert entity.description == "Demo"
    #
    # # Assert all fields are optional (partial=True)
    assert PartialEntity.model_fields["id"].annotation == (str | None)
    assert PartialEntity.model_fields["name"].annotation == (str | None)
    assert PartialEntity.model_fields["description"].annotation == (str | None)
    assert ["id", "name", "description"] == list(PartialEntity.model_fields.keys())

    entity2 = PartialEntity()
    print(entity2)
    assert entity2.id is None
    assert entity2.name is None
    assert entity2.description is None
    #
    # # Check config
    assert hasattr(PartialEntity.Config, "from_attributes")
    assert PartialEntity.Config.from_attributes is False
    #
    # # Check example in config
    example = getattr(PartialEntity.Config, "json_schema_extra", {}).get("example")
    assert example["id"] == "entity_123"
    assert example["name"] == "Sample Entity"
    assert (
        example["description"] == "This is a sample entity for demonstration purposes."
    )

    print("All assertions passed.")
