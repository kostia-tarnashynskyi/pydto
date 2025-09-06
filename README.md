# pydto

Helper for creating DTO models from Pydantic v2 models, inspired by TypeScript utilities: Pick, Omit, Partial, Rename.

## Features

- Create DTOs using Pick, Omit, Partial, Rename
- Type-safe, compatible with Pydantic v2
- Simple decorator API

## Installation

```bash
pip install pydto
```

## Usage

Suppose you have a Pydantic v2 model:
### Decorator Example
```python
from pydantic import BaseModel
from pydto import dto_model

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

@dto_model(pick_fields=["id", "name"])
class UserPublicDTO(User): pass

@dto_model(omit_fields=["password"])
class UserSafeDTO(User): pass

@dto_model(partial=True)
class UserPartialDTO(User): pass

@dto_model(rename_fields={"email": "contact_email"})
class UserRenamedDTO(User): pass

# Usage
user = User(id=1, name="Alice", email="alice@example.com", password="12345")
public_dto = UserPublicDTO.model_validate(user.model_dump())
safe_dto = UserSafeDTO.model_validate(user.model_dump())
partial_dto = UserPartialDTO.model_validate({"name": "Alice"})
renamed_dto = UserRenamedDTO.model_validate(user.model_dump())
```

### Factory Function Example
```python
from pydantic import BaseModel
from pydto import create_dto_model

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

UserPublicDTO = create_dto_model(User, pick_fields=["id", "name"])
UserSafeDTO = create_dto_model(User, omit_fields=["password"])
UserPartialDTO = create_dto_model(User, partial=True)
UserRenamedDTO = create_dto_model(User, rename_fields={"email": "contact_email"})
```

## Why?

- Inspired by TypeScript's Pick, Omit, Partial, Rename
- Keeps your DTOs simple and DRY


## Note 
- Requires Pydantic v2
- Only fields are inherited in the DTO model. Methods, validators, and computed properties from the base model are not included.
- Use for simple DTOs where field selection, omission, renaming, and partiality are needed.