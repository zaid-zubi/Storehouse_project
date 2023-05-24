from core.mongo.client import db
from core.settings.base import settings


async def get_mongo():
    """
    get async mongo client
    """

    return db.client


def get_mongo_database(database: str = settings.MONGO_DB_NAME):
    """
    get async mongo client
    """

    async def _get_mongo_database():
        return db.client[database]

    return _get_mongo_database
