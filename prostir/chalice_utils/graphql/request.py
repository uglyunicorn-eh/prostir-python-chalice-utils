import asyncio
import dataclasses
import logging
from typing import Optional

from chalice.app import Response, Request
import graphene
from graphql import ExecutionResult
from sentry_sdk import capture_exception

from .utils import extract_params, translate_result


def graphql_request(
    request: Request,
    *,
    schema: graphene.Schema,
    logger: Optional[logging.Logger] = None,
) -> Response:
    try:
        if (query_params := extract_params(request)) and not query_params.source:
            return Response(
                {
                    "code": "Success",
                    "message": None,
                    "errors": None,
                    "data": None,
                },
            )

        loop = asyncio.new_event_loop()
        res: ExecutionResult = loop.run_until_complete(
            schema.execute_async(
                **dataclasses.asdict(query_params),
            ),
        )
        return translate_result(res)
    except Exception as e:  # pylint: disable=broad-except
        capture_exception(e)
        logger = logger or logging.getLogger(__name__)
        logger.exception(e)
        return Response(
            {
                "code": "InternalServerError",
                "message": "The server has encountered a situation it does not know how to handle.",
                "errors": None,
                "data": None,
            },
            status_code=500,
        )
