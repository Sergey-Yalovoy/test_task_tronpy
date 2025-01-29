import asyncio
from datetime import time, datetime

from tronpy import Tron, AsyncTron
from tronpy.exceptions import AddressNotFound

async def gather_main():
    # Ваш адрес TRON
    address = "TVF2Mp9QY7FEGTnr3DBpFLobA6jguHyMvi"  # Замените на нужный адрес

    # Подключаемся к клиенту TRON
    client = AsyncTron(network='shasta')

    try:
        # Получаем баланс TRX  # Использованный Bandwidth
        tasks = [client.get_account_balance(address),
                 client.get_account(address),
                 client.get_account_resource(address)
                 ]
        results = await asyncio.gather(*tasks)

        for r in results:
            print(r)

    except AddressNotFound:
        print("Адрес не найден или неактивен!")


if __name__ == '__main__':
    from config import settings
    print(settings.DB_PATH, settings.TRON_TOKEN, settings.TRON_NETWORK)
    asyncio.run(gather_main())