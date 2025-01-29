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
        self.repository = TronWalletRepository(session)
        if settings.TRON_TOKEN and settings.TRON_PROVIDER:
            self.client = AsyncTron(provider=AsyncHTTPProvider(settings.TRON_PROVIDER,
                                                               api_key=settings.TRON_TOKEN))
        else:
            self.client = AsyncTron(network=settings.TRON_NETWORK)

    async def get_all(self):
        return await self.repository.get_all(paginated_result=True,
                                             ordering_by_id='desc')

    async def get_data_from_tron_wallet_by_address(self, address: str) -> typing.List:
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