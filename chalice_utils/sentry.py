from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration


def setup_sentry(dsn: Optional[str]):
    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[AwsLambdaIntegration()],
        )
