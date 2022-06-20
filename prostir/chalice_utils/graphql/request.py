import asyncio
import dataclasses
import logging
from typing import Optional, Any

from chalice.app import Response, Request
import graphene
from graphql import ExecutionResult, Middleware, ExecutionContext
from sentry_sdk import capture_exception

from .utils import extract_params, translate_result
from .execute import ProstirExecutionContext


def graphql_request(
    request: Request,
    *,
    schema: graphene.Schema,
    context: Any,
    middleware: Optional[Middleware] = None,
    root_value: Optional[Any] = None,
    execution_context_class: Optional[type[ExecutionContext]] = ProstirExecutionContext,
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
                context=context,
                middleware=middleware,
                root_value=root_value,
                execution_context_class=execution_context_class,
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
