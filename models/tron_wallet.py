from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base, BaseDBMixin


class TronWallet(Base, BaseDBMixin):
    address: Mapped[str] = mapped_column()
    balance: Mapped[Decimal] = mapped_column(Numeric(None, 6))
    # я использую эти поля намерено, потому что по ним можно будет рассчитать available
    free_net_used: Mapped[int]
    free_net_limit: Mapped[int]
    energy_limit: Mapped[int]
    energy_used: Mapped[int]

    @property
    def energy_available(self) -> int:
        return self.energy_limit - self.energy_used

    @property
    def available_bandwidth(self) -> int:
        return self.free_net_limit - self.free_net_used


