from datetime import datetime
from functools import reduce

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.orm import declarative_mixin


def change_case(input_string: str) -> str:
    return reduce(
        lambda x, y: x + ("_" if y.isupper() else "") + y, input_string
    ).lower()


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return change_case(cls.__name__)


@declarative_mixin
class BaseDBMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
