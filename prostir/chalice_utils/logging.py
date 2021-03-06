import datetime
import json
import logging
from typing import Optional
from collections.abc import Callable


def _json_serialize_default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

    return repr(o)


class CloudWatchLogFormatter(logging.Formatter):
    def __init__(
        self,
        *args,
        json_serialize_default: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.json_serialize_default = json_serialize_default or _json_serialize_default

    def format(self, record: logging.LogRecord):
        s = super().format(record)

        res = {
            "record": {
                "level": record.levelname,
                "funcName": record.funcName,
                "lineno": record.lineno,
                "file": record.pathname,
            },
            "message": s,
        }

        return json.dumps(res, default=self.json_serialize_default)


def setup_logging(
    logger: Optional[logging.Logger] = None,
    *,
    level: int = logging.INFO,
):
    logger = logger or logging.getLogger("root")
    for h in logger.handlers:
        h.setFormatter(CloudWatchLogFormatter())
    logger.setLevel(level)
