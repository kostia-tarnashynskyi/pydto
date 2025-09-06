import pytest
from pydantic import BaseModel, ConfigDict

from src.pydto.pydantic_v2 import create_dto_model, dto_model


def test_dto_model_pick_fields():
    class Base(BaseModel):
        a: int
        b: str
        c: float

    @dto_model(pick_fields=["a", "c"])
    class DTO(Base):
        ...

    assert set(DTO.model_fields.keys()) == {"a", "c"}

def test_dto_model_omit_fields():
    class Base(BaseModel):
        x: int
        y: str
        z: float

    @dto_model(omit_fields=["y"])
    class DTO(Base):
        ...

    assert set(DTO.model_fields.keys()) == {"x", "z"}

def test_dto_model_rename_fields():
    class Base(BaseModel):
        foo: int
        bar: str

    @dto_model(rename_fields={"foo": "baz"})
    class DTO(Base):
        ...

    assert "baz" in DTO.model_fields
    assert "foo" not in DTO.model_fields

def test_dto_model_partial_fields():
    class Base(BaseModel):
        id: int
        name: str

    @dto_model(partial=True)
    class DTO(Base):
        ...

    assert DTO.model_fields["id"].annotation == (int | None)
    assert DTO.model_fields["name"].annotation == (str | None)
    dto = DTO()
    assert dto.id is None
    assert dto.name is None

def test_dto_model_config_dict():
    class Base(BaseModel):
        id: int

    config = ConfigDict(title="CustomDTO")
    @dto_model(config=config)
    class DTO(Base):
        ...

    assert DTO.model_config["title"] == "CustomDTO"

def test_dto_model_error_on_missing_field():
    class Base(BaseModel):
        id: int

    with pytest.raises(ValueError):
        @dto_model(pick_fields=["missing"])
        class DTO(Base):
            ...


# Tests for create_dto_model function
def test_create_dto_model_pick_fields():
    class Base(BaseModel):
        a: int
        b: str
        c: float

    DTO = create_dto_model(Base, pick_fields=["a", "c"])
    assert set(DTO.model_fields.keys()) == {"a", "c"}

def test_create_dto_model_omit_fields():
    class Base(BaseModel):
        x: int
        y: str
        z: float

    DTO = create_dto_model(Base, omit_fields=["y"])
    assert set(DTO.model_fields.keys()) == {"x", "z"}

def test_create_dto_model_rename_fields():
    class Base(BaseModel):
        foo: int
        bar: str

    DTO = create_dto_model(Base, rename_fields={"foo": "baz"})
    assert "baz" in DTO.model_fields
    assert "foo" not in DTO.model_fields

def test_create_dto_model_partial_fields():
    class Base(BaseModel):
        id: int
        name: str

    DTO = create_dto_model(Base, partial=True)
    assert DTO.model_fields["id"].annotation == (int | None)
    assert DTO.model_fields["name"].annotation == (str | None)
    dto = DTO()
    assert dto.id is None
    assert dto.name is None

def test_create_dto_model_config_dict():
    class Base(BaseModel):
        id: int

    config = ConfigDict(title="CustomDTO")
    DTO = create_dto_model(Base, config=config)
    assert DTO.model_config["title"] == "CustomDTO"

def test_create_dto_model_error_on_missing_field():
    class Base(BaseModel):
        id: int

    with pytest.raises(ValueError):
        create_dto_model(Base, pick_fields=["missing"])
