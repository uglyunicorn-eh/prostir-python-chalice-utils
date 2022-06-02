import json
from typing import Any

from chalice.app import Request


def parse_body(request: Request) -> dict[str, Any]:
    content_type = request.headers.get("Content-Type")

    if content_type == "application/graphql":
        return {"query": request.raw_body}

    try:
        return json.loads(request.raw_body)
    except ValueError:
        return {}
