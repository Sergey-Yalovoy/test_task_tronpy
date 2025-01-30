import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from repository import TronWalletRepository


@pytest.mark.asyncio
async def test_get_all_wallets_api(override_get_async_session):
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        response = await client.get("/wallet/get_all")

    assert response.status_code == 200
    assert "items" in response.json()


@pytest.mark.asyncio
async def test_create_wallet_api(override_get_async_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        data = {"address": "TLRwhvNxnDjCDFo6YS6Vkbn5uo59CQM4Lf"}
        response = await client.post("/wallet/", json=data)

    assert response.status_code == 200
    wallet = response.json()
    assert "id" in wallet
    assert "balance" in wallet
    assert "free_net_used" in wallet
    assert "free_net_limit" in wallet
    assert "energy_limit" in wallet
    assert "energy_used" in wallet
    assert "energy_available" in wallet
    assert "available_bandwidth" in wallet


@pytest.mark.asyncio
async def test_create_wallet(wallet_repository: TronWalletRepository):
    wallet_data = {
        "address": "TLRwhvNxnDjCDFo6YS6Vkbn5uo59CQM4Lf",
        "balance": 100.50,
        "free_net_used": 100,
        "free_net_limit": 5000,
        "energy_limit": 10000,
        "energy_used": 500
    }

    wallet = await wallet_repository.create(wallet_data)

    assert wallet.id is not None
    assert wallet.address == "TLRwhvNxnDjCDFo6YS6Vkbn5uo59CQM4Lf"
    assert wallet.balance == 100.50
    assert wallet.energy_available == 9500  # energy_limit - energy_used
    assert wallet.available_bandwidth == 4900
