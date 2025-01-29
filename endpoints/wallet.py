import typing

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from schemas.tron_wallet import TronWalletBase, TronWalletRequest
from service.tron_wallet import get_tron_wallet_service, TronWalletService

wallet_router = APIRouter(prefix="/wallet", tags=["tron-wallet"])


@wallet_router.get("/get_all")
async def get_all(wallet_service: typing.Annotated[TronWalletService,
Depends(get_tron_wallet_service)]) -> Page[TronWalletBase]:
    return await wallet_service.get_all()


@wallet_router.post("/", response_model=TronWalletBase)
async def create_sub_catalog(data: TronWalletRequest,
                             wallet_service: typing.Annotated[TronWalletService,
                             Depends(get_tron_wallet_service)]):
    return await wallet_service.get_from_address(data.address)
