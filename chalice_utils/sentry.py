from typing import Optional

import sentry_sdk


_sentry_setup = False


def setup_sentry(
    *,
    dsn: Optional[str],
):
    from sentry_sdk.integrations.chalice import ChaliceIntegration

    global _sentry_setup
    if _sentry_setup:
        return

    _sentry_setup = True

    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[ChaliceIntegration()],
        )
