import asyncio
import dataclasses
import json
import logging
from typing import Any, Dict, Optional, cast

from chalice.app import Response, Request
import graphene
from graphql import ExecutionResult
from sentry_sdk import capture_exception

from chalice_utils.json import handle_extra_types
from chalice_utils.request import parse_body


class CustomResponse(Response):
    def to_dict(self, binary_types=None):
        body = self.body
        if not isinstance(body, (str, bytes)):
            body = json.dumps(body, separators=(",", ":"), default=handle_extra_types)
        single_headers, multi_headers = self._sort_headers(self.headers)  # type: ignore
        response = {
            "headers": single_headers,
            "multiValueHeaders": multi_headers,
            "statusCode": self.status_code,
            "body": body,
        }
        if binary_types is not None:
            self._b64encode_body_if_needed(response, binary_types)  # type: ignore
        return response


def translate_result(res: ExecutionResult) -> Response:
    return CustomResponse(
        {
            "data": res.data,
            **(
                {
                    "code": "Success",
                    "message": None,
                    "errors": None,
                }
                if res.errors is None
                else {
                    "code": res.errors[0].__class__.__name__,
                    "message": "A GraphQL error occurred.",
                    "errors": res.errors,
                }
            ),
        },
        status_code=200 if res.errors is None else 400,
    )


@dataclasses.dataclass(frozen=True)
class GraphQLParams:
    source: str
    variable_values: Optional[Dict[str, Any]]
    operation_name: Optional[str]


def extract_params(request: Request) -> GraphQLParams:
    data = parse_body(request)
    query_data = request.query_params or {}

    return GraphQLParams(
        source=data.get("query") or query_data.get("query") or "",
        variable_values=cast(Dict[str, Any], data.get("variables") or query_data.get("variables") or {}),
        operation_name=data.get("operationName") or query_data.get("operationName"),
    )


def graphql_request(request: Request, *, schema: graphene.Schema) -> Response:
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
    except Exception as e:
        capture_exception(e)
        logging.getLogger(__name__).exception(e)
        return Response(
            {
                "code": "InternalServerError",
                "message": "The server has encountered a situation it does not know how to handle.",
                "errors": None,
                "data": None,
            },
            status_code=500,
        )
