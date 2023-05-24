from datetime import datetime 
import logging

# from fastapi_versioning import VersionedFastAPI

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.routers import api_router
from core import mongo
from core.middlewares.catch_exception import ExceptionMiddleWare
from integrations.aws_queue.sqs_consumer import sqs_event_listener

logger = logging.getLogger(__name__)

app = FastAPI(title="Skeleton", docs_url="/skeleton/docs",
              openapi_url="/skeleton/openapi.json")


@app.middleware("http")
async def log_request_time(request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    elapsed_time = datetime.now() - start_time
    print(f"Request received at {start_time}. Elapsed time: {elapsed_time}")
    return response

# CORS
origins = []

# Set all CORS enabled origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ExceptionMiddleWare)
app.include_router(api_router)


# app.add_event_handler('startup', sqs_event_listener)
# app.add_event_handler('startup', mongo.events.connect_to_mongo)
# app.add_event_handler('shutdown', mongo.events.close_mongo_connection)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Skeleton",
        version="1.0.0",
        description="The documentation for Skeleton service",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app)
