import dataclasses
import json
from typing import Any, Optional, cast

from chalice.app import Response, Request
from graphql import ExecutionResult

from .response import CustomResponse


@dataclasses.dataclass(frozen=True)
class GraphQLParams:
    source: str
    variable_values: Optional[dict[str, Any]]
    operation_name: Optional[str]


def parse_body(request: Request) -> dict[str, Any]:
    if request.headers.get("Content-Type") == "application/graphql":
        query = (request.raw_body or b"").decode()
        return {"query": query}

    try:
        return json.loads(request.raw_body) if request.raw_body else {}
    except ValueError:
        return {}


def extract_params(request: Request) -> GraphQLParams:
    data = parse_body(request)
    query_data = request.query_params or {}

    return GraphQLParams(
        source=data.get("query") or query_data.get("query") or "",
        variable_values=cast(dict[str, Any], data.get("variables") or query_data.get("variables") or {}),
        operation_name=data.get("operationName") or query_data.get("operationName"),
    )


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
