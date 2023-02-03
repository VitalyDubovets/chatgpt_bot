import logging
import sys
from enum import Enum
from logging import config
from typing import Union

import orjson
import structlog
from structlog.contextvars import merge_contextvars


class LogFormat(str, Enum):
    JSON = "json"
    CONSOLE = "console"


def add_log_location_data(logger, _, event_dict: dict) -> dict:
    record = event_dict.get("_record")
    if record is not None:
        event_dict["filepath"] = record.pathname
        event_dict["module"] = record.module
        event_dict["function"] = record.funcName
        event_dict["lineno"] = record.lineno
    elif logger is not None:
        from structlog._frames import _find_first_app_frame_and_name

        frame, _ = _find_first_app_frame_and_name(["logging", __name__])
        event_dict["filepath"] = frame.f_code.co_filename
        event_dict["module"] = frame.f_globals["__name__"]
        event_dict["function"] = frame.f_code.co_name
        event_dict["lineno"] = frame.f_lineno
    return event_dict


def configure_logging(log_level: Union[int, str] = logging.INFO, log_format: LogFormat = LogFormat.JSON):
    root_logger = logging.getLogger()
    root_logger.handlers = []

    timestamper = structlog.processors.TimeStamper(fmt="iso")
    pre_chain = [
        # Add the log level and a timestamp to the event_dict if the log entry
        # is not from structlog.
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        add_log_location_data,
        timestamper,
        structlog.processors.format_exc_info,
    ]

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level)

    config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                LogFormat.CONSOLE: {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.dev.ConsoleRenderer(colors=True),
                    ],
                    "foreign_pre_chain": pre_chain,
                },
                LogFormat.JSON: {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(serializer=orjson.dumps),
                    "foreign_pre_chain": pre_chain,
                },
            },
            "handlers": {
                "default": {
                    "level": log_level,
                    "class": "logging.StreamHandler",
                    "formatter": log_format,
                },
            },
            "loggers": {
                "": {
                    "handlers": [
                        "default",
                    ],
                    "level": log_level if isinstance(log_level, str) else logging.getLevelName(log_level),
                    "propagate": True,
                },
            },
        }
    )

    if log_format == LogFormat.JSON:
        renderer = structlog.processors.JSONRenderer(serializer=orjson.dumps)
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.format_exc_info,
            renderer,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
