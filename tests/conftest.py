import logging

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from db.session import get_async_session
from main import app
from models.base_model import Base
from repository import TronWalletRepository

# Создаём тестовый движок SQLite (или другую тестовую БД)
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DB_URL, echo=True)  # Включаем echo для отладки
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    """Фикстура для создания тестовой сессии."""
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    """Создаёт и очищает таблицы перед каждым тестом."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        # Очищаем после тестов
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def override_get_async_session(async_session: AsyncSession):
    """Подменяем get_async_session на тестовую версию."""

    async def _override():
        yield async_session

    app.dependency_overrides[get_async_session] = _override
    yield
    # Очищаем override после использования
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def wallet_repository(async_session: AsyncSession):
    """Фикстура для создания репозитория"""
    return TronWalletRepository(async_session)
