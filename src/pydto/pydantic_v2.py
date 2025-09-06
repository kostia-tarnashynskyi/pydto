from pydantic import create_model


def dto(
    partial: bool = False,
    pick_fields: list[str] | None = None,
    omit_fields: list[str] | None = None,
    rename_fields: dict[str, str] | None = None,
    config: dict | None = None,
):
    def decorator(cls):
        # Create a new dictionary to hold the fields for the new model
        fields = {}
        for field_name, model_field in cls.model_fields.items():
            if pick_fields and field_name not in pick_fields:
                continue
            if omit_fields and field_name in omit_fields:
                continue
            new_field_name = (
                rename_fields.get(field_name, field_name)
                if rename_fields
                else field_name
            )
            fields[new_field_name] = (model_field.annotation, model_field.default)

        # If partial is True, make all fields optional
        if partial:
            for field_name in fields:
                annotation, default = fields[field_name]
                default = None  # Make field optional
                fields[field_name] = (annotation | None, default)

        # Create a new Pydantic model with the modified fields
        new_model = create_model(cls.__name__, __base__=cls, **fields)

        # Apply additional config if provided
        if config:
            new_model.Config = type("Config", (), config)

        return new_model

    return decorator
