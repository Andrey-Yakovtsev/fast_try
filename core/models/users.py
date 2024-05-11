from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.models.base import Base


class User(Base):
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[Optional[List["Address"]]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    city: Mapped[str] = mapped_column(String(30))
    street: Mapped[str] = mapped_column(String(30))
    house: Mapped[str] = mapped_column(Integer())
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional[User]] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, city={self.city!r}, user={self.user!r})"
