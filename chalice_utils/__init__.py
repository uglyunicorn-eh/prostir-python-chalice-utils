from typing import Optional
from chalicelib.utils.logging import setup_logging
from chalicelib.utils.sentry import setup_sentry


def setup_chalice(
    *,
    sentry_dsn: Optional[str],
):
    setup_sentry(sentry_dsn)
    setup_logging()
