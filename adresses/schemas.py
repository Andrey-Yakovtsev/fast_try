from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict



class BaseAddressModel(BaseModel):
    city: str = Annotated[str, MinLen(3), MaxLen(30)]
    street: str = Annotated[str, MinLen(3), MaxLen(30)]
    house: int
    user_id: int

class CreateAddress(BaseAddressModel):
    ...


class AddressSchema(BaseAddressModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


