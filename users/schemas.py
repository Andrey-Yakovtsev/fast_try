from typing import Optional, Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class BaseUserModel(BaseModel):
    name: str = Annotated[str, MinLen(3), MaxLen(10)]
    fullname: str | None


class CreateUser(BaseUserModel):
    ...


class UserSchema(CreateUser):
    model_config = ConfigDict(from_attributes=True)
    id: int


