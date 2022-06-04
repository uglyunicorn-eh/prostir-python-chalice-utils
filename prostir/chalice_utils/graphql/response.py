import decimal
import json
from typing import Any

from chalice.app import Response
from graphql.error import GraphQLError


def handle_extra_types(obj: Any) -> Any:
    if isinstance(obj, GraphQLError):
        return obj.formatted

    if isinstance(obj, decimal.Decimal):
        return f"{obj:.2f}"

    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


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
