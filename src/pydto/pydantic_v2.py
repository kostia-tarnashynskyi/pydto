from typing import TypeVar, cast

from pydantic import BaseModel, ConfigDict, create_model

T = TypeVar("T", bound=BaseModel)


def dto_model(
    partial: bool = False,
    pick_fields: list[str] | None = None,
    omit_fields: list[str] | None = None,
    rename_fields: dict[str, str] | None = None,
    config: ConfigDict | None = None,
    model_name: str | None = None
):
    """ Pydantic v2 DTO decorator: Pick, Omit, Rename, Partial, Config
    Args:
        pick_fields: list of fields to include (if None — all fields)
        omit_fields: list of fields to exclude
        rename_fields: {old: new field name}
        partial: if True, all fields become Optional
        config: ConfigDict for model configuration
        model_name: name of the new model

    Returns:
        New Pydantic model type
    """

    pick_fields = pick_fields or []
    omit_fields = omit_fields or []
    rename_fields = rename_fields or {}

    def decorator(cls: type[T]) -> type[T]:
        base_fields = cls.model_fields

        # if pick is None, get all fields
        field_names = pick_fields or list(base_fields.keys())

        # Remove omitted fields
        field_names = [f for f in field_names if f not in omit_fields]

        dto_fields: dict[str, tuple] = {}
        for orig_name in field_names:
            if orig_name not in base_fields:
                raise ValueError(f"Field '{orig_name}' not in base model {cls.__name__}")
            dto_field = base_fields[orig_name]

            # Rename field if needed
            new_name = rename_fields.get(orig_name, orig_name)

            annotation = dto_field.annotation
            default = dto_field.default if dto_field.default is not None else ...
            if partial:
                annotation = annotation | None
                default = None
            dto_fields[new_name] = (annotation, default)

        # Define model name, default decorated class name
        dto_cls_name = model_name or cls.__name__

        # Pydantic v2 create_model
        new_dto_model = create_model(
            dto_cls_name,
            **dto_fields
        )
        if config:
            new_dto_model.model_config = config
        return cast(type[T], new_dto_model)

    return decorator


def create_dto_model(
    base_model: type[T],
    partial: bool = False,
    pick_fields: list[str] | None = None,
    omit_fields: list[str] | None = None,
    rename_fields: dict[str, str] | None = None,
    config: ConfigDict | None = None,
    model_name: str | None = None
) -> type[T]:
    """ Pydantic v2 DTO factory function: Pick, Omit, Rename, Partial, Config
    Args:
        base_model: Base Pydantic model class
        pick_fields: list of fields to include (if None — all fields)
        omit_fields: list of fields to exclude
        rename_fields: {old: new field name}
        partial: if True, all fields become Optional
        config: ConfigDict for model configuration
        model_name: name of the new model

    Returns:
        New Pydantic model type
    """
    return dto_model(
        partial=partial,
        pick_fields=pick_fields,
        omit_fields=omit_fields,
        rename_fields=rename_fields,
        config=config,
        model_name=model_name
    )(base_model)
