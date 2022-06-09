from typing import Optional

import sentry_sdk


_sentry_setup = False


def setup_sentry(
    *,
    dsn: Optional[str],
    release: Optional[str] = None,
    environment: Optional[str] = None,
):
    from sentry_sdk.integrations.chalice import ChaliceIntegration  # pylint: disable=import-outside-toplevel

    global _sentry_setup  # pylint: disable=global-statement
    if _sentry_setup:
        return

    _sentry_setup = True

    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[ChaliceIntegration()],
            release=release,
            environment=environment,
        )
