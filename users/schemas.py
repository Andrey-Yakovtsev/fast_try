from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class BaseUserModel(BaseModel):
    name: str = Annotated[str, MinLen(3), MaxLen(10)]
    fullname: str = Annotated[str, MinLen(3), MaxLen(10)]


class CreateUser(BaseUserModel):
    ...


class UserSchema(BaseUserModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


