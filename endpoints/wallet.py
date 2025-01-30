import typing

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from schemas.tron_wallet import TronWalletBase, TronWalletRequest
from service.tron_wallet import get_tron_wallet_service, TronWalletService

wallet_router = APIRouter(prefix="/wallet", tags=["tron-wallet"])


@wallet_router.get("/get_all",
                   summary="Получить все кошельки",
                   description="Возвращает список всех кошельков Tron из базы данных с пагинацией. "
                               "Кошельки сортируются по ID в порядке убывания.",
                   response_description="Список кошельков с пагинацией."
                   )
async def get_all(wallet_service: typing.Annotated[TronWalletService,
Depends(get_tron_wallet_service)]) -> Page[TronWalletBase]:
    """
        Получить все кошельки.

        Returns:
            Page[TronWalletBase]: Пагинированный список кошельков.
        """
    return await wallet_service.get_all()


@wallet_router.post("/",
                    response_model=TronWalletBase,
                    summary="Создать или обновить кошелек",
                    description="Получает данные о кошельке Tron по указанному адресу и сохраняет их в базе данных. "
                                "Если кошелек с таким адресом уже существует, он будет обновлен.",
                    response_description="Данные сохраненного или обновленного кошелька."
                    )
async def create_sub_catalog(data: TronWalletRequest,
                             wallet_service: typing.Annotated[TronWalletService,
                             Depends(get_tron_wallet_service)]):
    """
        Создать или обновить кошелек.

        Args:
            data (TronWalletRequest): Запрос с адресом кошелька Tron.

        Returns:
            TronWalletBase: Данные кошелька, сохраненного в базе данных.

        Raises:
            HTTPException: Если адрес не найден или произошла ошибка при загрузке данных.
        """
    return await wallet_service.get_from_address(data.address)
