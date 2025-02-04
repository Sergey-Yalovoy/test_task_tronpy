# Tron Wallet Service

Этот проект представляет собой сервис для работы с кошельками сети Tron. Он позволяет получать данные о кошельках, такие как баланс, использование ресурсов (энергия и пропускная способность), и сохранять их в базе данных. Проект поддерживает работу как с тестовой сетью Shasta, так и с основной сетью Tron через API провайдера.

## Зависимости

Для работы проекта необходимо установить следующие зависимости:

- Python 3.12 или выше
- Библиотеки, указанные в `requirements.txt` или в `pyproject.toml`

Создайте виртуальное окружение:

```bash
python3 -m venv env
```


Установите зависимости с помощью команды:

```bash
pip install -r requirements.txt
```
Или

```bash
pip install poetry
poetry install
```

## Настройка окружения

Перед запуском проекта создайте файл `.env` в корневой директории и укажите в нем следующие переменные:

```env
DB_PATH=sqlite+aiosqlite:///:memory:
TRON_NETWORK=shasta
TRON_TOKEN=<your token - optional>
TRON_PROVIDER=https://api.trongrid.io
```

### Описание переменных окружения:

- **`DB_PATH`**: Путь к базе данных. По умолчанию используется SQLite в памяти.
- **`TRON_NETWORK`**: Сеть Tron, с которой будет работать проект. Возможные значения:
  - `shasta` (тестовая сеть)
  - `mainnet` (основная сеть)
- **`TRON_TOKEN`**: API-токен для доступа к провайдеру Tron (опционально, если используется `TRON_PROVIDER`).
- **`TRON_PROVIDER`**: URL провайдера API Tron. По умолчанию используется `https://api.trongrid.io`.

## Запуск проекта

1. Убедитесь, что все зависимости установлены и файл `.env` настроен.
2. Запустите проект с помощью команды:

```bash
python main.py
```

Сервис будет доступен по адресу: `http://0.0.0.0:8000`.

Swagger будет доступен по адресу:`http://localhost:8000/docs#/`.

## Запуск тестов

Тесты написаны для работы с сетью `api.trongrid.io`. В тестах используется тестовый кошелек `TLRwhvNxnDjCDFo6YS6Vkbn5uo59CQM4Lf`, который можно заменить на любой другой для проверки.

Для запуска тестов выполните команду:

```bash
pytest
```

### Описание тестов:

1. **`test_get_all_wallets_api`**: Проверяет эндпоинт `/wallet/get_all`, который возвращает список всех кошельков.
2. **`test_create_wallet_api`**: Проверяет эндпоинт `/wallet/`, который создает или обновляет кошелек по указанному адресу.
3. **`test_create_wallet`**: Проверяет создание кошелька через репозиторий.

## Использование API

### Получить все кошельки

**Запрос:**

```bash
GET /wallet/get_all
```

**Ответ:**

```json
{
  "items": [
    {
      "id": 1,
      "address": "TLRwhvNxnDjCDFo6YS6Vkbn5uo59CQM4Le",
      "balance": 100.5,
      "free_net_used": 100,
      "free_net_limit": 5000,
      "energy_limit": 10000,
      "energy_used": 500,
      "energy_available": 9500,
      "available_bandwidth": 4900
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10
}
```

### Получить информацию о кошельке и сохранить запрос в БД

**Запрос:**

```bash
POST /wallet/
```

**Тело запроса:**

```json
{
  "address": "TLRwhvNxnDjCDFo6YS6Vkbn5uo59CQM4Le"
}
```

**Ответ:**

```json
{
  "id": 1,
  "address": "TLRwhvNxnDjCDFo6YS6Vkbn5uo59CQM4Le",
  "balance": 100.5,
  "free_net_used": 100,
  "free_net_limit": 5000,
  "energy_limit": 10000,
  "energy_used": 500,
  "energy_available": 9500,
  "available_bandwidth": 4900
}
```

## Примечания

- Для работы с основной сетью Tron укажите `TRON_NETWORK=mainnet` и предоставьте API-токен в `TRON_TOKEN`.
- Если вы используете тестовую сеть Shasta, убедитесь, что адрес кошелька принадлежит этой сети.
- В тестах используется фиктивный кошелек. Замените его на реальный для проверки в основной сети.

---
