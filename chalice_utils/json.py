import decimal
from typing import Any

from graphql.error import GraphQLError


def handle_extra_types(obj: Any) -> Any:
    if isinstance(obj, GraphQLError):
        return obj.formatted

    if isinstance(obj, decimal.Decimal):
        return f"{obj:.2f}"

    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
