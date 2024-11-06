from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    USE_RANDOM_DELAY_IN_RUN: bool = False
    RANDOM_DELAY_IN_RUN: list[int] = [0, 3600]

    USE_PROXY: bool = False

    SET_AVATAR: bool = False
    SET_BIO: bool = False

    SET_EMOJI: bool = False
    EMOJI_TO_SET: Optional[str] = "🌟"
    DELETE_ALL_EMOJI: bool = True

    AVATAR_DELAY_RANGE: list[float] = [48, 96]  # 48-96 hours
    BIO_DELAY_RANGE: list[float] = [48, 96]  # 48-96 hours

    PARSE_ALL_CHATS: bool = False
    PARSE_ALL_CHATS_SESSION: Optional[str] = ""


settings = Settings()
