import logging
from typing import Any, Optional, Union

import structlog
from pydantic import BaseSettings, Extra, RedisDsn, validator

from src.infrstructure.log import LogFormat

logger = structlog.get_logger(__name__)


class Settings(BaseSettings):
    TG_TOKEN: str
    OPENAI_API_TOKEN: str

    LOG_LEVEL: Union[str, int] = logging.INFO
    LOG_FORMAT: LogFormat = LogFormat.CONSOLE

    REDIS_HOST: str = ""
    REDIS_PORT: int = 27017
    REDIS_PASSWORD: str
    REDIS_URI: Optional[RedisDsn] = None

    @validator("REDIS_URI", pre=True, allow_reuse=True)
    def assemble_redis_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            password=values.get("REDIS_PASSWORD"),
            host=values.get("REDIS_HOST"),
            port=str(values.get("REDIS_PORT")),
        )

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = Extra.ignore


settings: Settings = Settings()
