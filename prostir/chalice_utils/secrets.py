import base64
import json
from typing import Any

import boto3


def get_secrets_aws(
    secret_name: str,
    *,
    region_name: str = "us-west-2",
) -> dict[str, Any]:
    session = boto3.session.Session()  # type: ignore
    client = session.client(service_name="secretsmanager", region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
    else:
        secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    secret_dict = json.loads(secret)
    return secret_dict
