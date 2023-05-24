import json
import logging
import time

from fastapi import status, Request, Response

from core.settings.base import settings, AppEnvTypes

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    wrap = "\""
    if 'beat' not in request.url.path and '/docs' not in request.url.path and '/openapi.json' not in request.url.path and settings.env != AppEnvTypes.prod:
        logger.info(f"{wrap}request: {request.method} {request.url.path} {request.url.query}{wrap}")
        print("request body:", Request.body.__dict__)
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        print("Response:")
        logger.info(f"{wrap}response: {response.status_code} in {formatted_process_time}ms{wrap}")
    else:
        return await call_next(request)

    response_body = b''
    async for chunk in response.body_iterator:
        response_body += chunk

    if 'beat' not in request.url.path:
        logger.info(response_body)
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )
