import asyncio
from src.core.db_helper import es

HISTORY_INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
            },
            "date": {"type": "date"},
            "pacientId": {"type": "keyword"},
            "hospitalId": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
            },
            "doctorId": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
            },
            "room": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
            },
            "data": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
            }
        }
    }
}


async def wait_for_elasticsearch():
    try:
        if await es.ping():
            print("Успешное подключение к ElasticSearch")
            return
        print("Elasticsearch не отвечает")
    except Exception as e:
        print(f"Ошибка при подключении к Elasticsearch: {e}")


async def create_index_if_not_exists():
    if not await es.indices.exists(index='history'):
        await es.indices.create(index="history", body=HISTORY_INDEX_MAPPING)
        print("Индекс 'history' создан")
