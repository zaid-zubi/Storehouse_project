import logging
import pathlib

import pymongo
from core.settings.base import settings
from core.mongo.client import db

logger = logging.getLogger(__name__)


async def connect_to_mongo():
    logger.info(f"connecting to mongo")
    path = pathlib.Path(__file__).parent.resolve()

    db.client = pymongo.MongoClient(
        'mongodb://administrator:test1234@docdb-2022-09-12-09-14-11.cluster-cbhxvcxuv83a.eu-central-1.docdb.amazonaws.com:27017',
        tls=True,
        tlsCAFile=str(path) + '/rds-combined-ca-bundle.pem')

    logger.info(f"connected to mongo")


async def close_mongo_connection():
    logger.info("closing connecting with mongo")

    db.client.close()

    logger.info("mongo connecting closed")
