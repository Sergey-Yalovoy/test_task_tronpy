from typing import Type, TypeVar, Generic, List, Optional, Literal

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta
from fastapi_pagination.ext.sqlalchemy import paginate

from models.tron_wallet import TronWallet

T = TypeVar("T", bound=DeclarativeMeta)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        """
        Инициализация репозитория с заданной моделью и сессией.

        :param model: Модель SQLAlchemy, с которой будет работать репозиторий.
        :param session: Сессия SQLAlchemy для выполнения запросов к базе данных.
        """
        self.model = model
        self.session = session

    async def get(self, obj_id: int) -> Optional[T]:
        """
        Получить объект по его идентификатору.

        :param obj_id: Идентификатор объекта, который нужно получить.
        :return: Объект модели, если найден, или None, если не найден.
        """
        result = await self.session.get(self.model, obj_id)
        return result

    async def get_all(self, paginated_result: bool = False,
                      ordering_by_id: Literal["desc", "asc"] = "asc") -> List[T]:
        """
        Получить все объекты модели, с возможностью сортировки и пагинации.
        P.S. Не стал использовать fastApi-filter поэтому сортировку сделал по-простому :)
        :param paginated_result: Флаг, указывающий, нужно ли возвращать результаты с пагинацией.
        :param ordering_by_id: Параметр для сортировки по идентификатору, может быть "asc" (по возрастанию) или "desc" (по убыванию).
        :return: Список объектов модели, отсортированных по идентификатору, с учетом пагинации, если указано.
        """
        stmt = select(self.model)
        if ordering_by_id == "desc":
            stmt = stmt.order_by(desc(self.model.id))
        else:
            stmt = stmt.order_by(self.model.id)
        if not paginated_result:
            result = await self.session.execute(stmt)
            return result.scalars().all()
        return await paginate(self.session, stmt)

    async def create(self, obj_in: dict) -> T:
        """
        Создать новый объект в базе данных.

        :param obj_in: Словарь данных для создания объекта, где ключи — это имена полей модели, а значения — данные для этих полей.
        :return: Созданный объект модели.
        """
        obj = self.model(**obj_in)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj_id: int, obj_in: dict) -> Optional[T]:
        """
        Обновить объект по его идентификатору.

        :param obj_id: Идентификатор объекта, который нужно обновить.
        :param obj_in: Словарь новых данных для объекта, где ключи — это имена полей модели, а значения — новые значения.
        :return: Обновленный объект, если он найден и успешно обновлен, или None, если объект не найден.
        """
        obj = await self.get(obj_id)
        if not obj:
            return None
        for key, value in obj_in.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool:
        """
        Удалить объект по его идентификатору.

        :param obj_id: Идентификатор объекта, который нужно удалить.
        :return: True, если объект был найден и удален, или False, если объект не найден.
        """
        obj = await self.get(obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

class TronWalletRepository(BaseRepository[TronWallet]):
    def __init__(self, session: AsyncSession):
        super().__init__(TronWallet, session)

