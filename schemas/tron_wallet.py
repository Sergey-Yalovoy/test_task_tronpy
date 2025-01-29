from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TronWalletBase(BaseModel):
    id: int
    balance: Decimal
    free_net_used: int
    free_net_limit: int
    energy_limit: int
    energy_used: int
    energy_available: int
    available_bandwidth: int
    model_config = ConfigDict(from_attributes=True)


class TronWalletRequest(BaseModel):
    address: str
