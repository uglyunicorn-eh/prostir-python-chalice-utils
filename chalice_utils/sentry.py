from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration


_sentry_setup = False


def setup_sentry(
    *,
    dsn: Optional[str],
):
    global _sentry_setup
    if _sentry_setup:
        return

    _sentry_setup = True

    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[AwsLambdaIntegration()],
        )
