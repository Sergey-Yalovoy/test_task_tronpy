import asyncio
import typing

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound, BadAddress
from tronpy.providers import AsyncHTTPProvider

from config import settings
from db.session import get_async_session
from models.tron_wallet import TronWallet
from repository import TronWalletRepository


class TronWalletService:
    def __init__(self, session: AsyncSession):
        """
        Инициализация сервиса для работы с кошельками Tron.

        Args:
           session (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.

        Инициализирует репозиторий для работы с кошельками и клиент для взаимодействия с сетью Tron.
        Если в настройках указаны TRON_TOKEN и TRON_PROVIDER, используется AsyncTron с провайдером и API-ключом.
        В противном случае используется сеть, указанная в TRON_NETWORK.
        """
        self.repository = TronWalletRepository(session)
        if settings.TRON_TOKEN and settings.TRON_PROVIDER:
            self.client = AsyncTron(provider=AsyncHTTPProvider(settings.TRON_PROVIDER,
                                                               api_key=settings.TRON_TOKEN))
        else:
            self.client = AsyncTron(network=settings.TRON_NETWORK)

    async def get_all(self):
        """
        Получение всех кошельков из базы данных.

        Returns:
           PaginatedResult: Пагинированный результат с кошельками, отсортированными по ID в порядке убывания.
        """
        return await self.repository.get_all(paginated_result=True,
                                             ordering_by_id='desc')

    async def get_data_from_tron_wallet_by_address(self, address: str) -> typing.List:
        """
        Получение данных о кошельке Tron по его адресу из сети Tron.

        Args:
        address (str): Адрес кошелька Tron.

        Returns:
        List: Список с данными о балансе и ресурсах аккаунта.

        Raises:
        HTTPException: Если адрес не найден или произошла ошибка при загрузке данных.
        """
        try:
            # Получаем баланс TRX  # Использованный Bandwidth
            tasks = [self.client.get_account_balance(address),
                     self.client.get_account_resource(address)
                     ]
            results = await asyncio.gather(*tasks)
            if len(results) != len(tasks):
                raise HTTPException(status_code=400,
                                    detail="Ошибка загрузки данных аккаунта tron")
            return results
        except (AddressNotFound, BadAddress):
            raise HTTPException(status_code=400,
                                detail="Адрес не найден или не верный")

    async def get_from_address(self, address: str) -> TronWallet:
        """
        Получение данных о кошельке Tron по адресу и сохранение их в базе данных.

        Args:
            address (str): Адрес кошелька Tron.

        Returns:
            TronWallet: Объект кошелька Tron, сохраненный в базе данных.

        Raises:
            HTTPException: Если адрес не найден или произошла ошибка при загрузке данных.
        """
        results = await self.get_data_from_tron_wallet_by_address(address)
        balance = results[0]
        account_resource = results[1]
        data_to_save = {"address": address,
                        "balance": balance,
                        "free_net_used": account_resource.get('freeNetUsed', 0),
                        "free_net_limit": account_resource.get('freeNetLimit', 0),
                        "energy_limit": account_resource.get('EnergyLimit', 0),
                        "energy_used": account_resource.get('EnergyUsed', 0),
                        }
        return await self.repository.create(data_to_save)


def get_tron_wallet_service(session: AsyncSession = Depends(get_async_session)):
    return TronWalletService(session=session)
