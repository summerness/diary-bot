import decouple
from functools import lru_cache
from pydantic_settings import BaseSettings


class BackendBaseSettings(BaseSettings):
    LSKY_URI: str = decouple.config('LSKY_URI', cast=str)
    LSKY_EMAIL: str = decouple.config('LSKY_EMAIL', cast=str)
    LSKY_PASSWORD: str = decouple.config('LSKY_PASSWD', cast=str)
    ALI_TOKEN: str = decouple.config('ALI_TOKEN', cast=str)
    PROMPT1: str = decouple.config('PROMPT1', cast=str)
    PROMPT2: str = decouple.config('PROMPT2', cast=str)
    PROMPT3: str = decouple.config('PROMPT3', cast=str)
    PROMPT4: str = decouple.config('PROMPT4', cast=str)
    HALO_URI: str = decouple.config('HALO_URI', cast=str)
    HALO_TOKEN: str = decouple.config('HALO_TOKEN', cast=str)


@lru_cache()
def get_settings() -> BackendBaseSettings:
    return BackendBaseSettings()  # type: ignore


settings: BackendBaseSettings = get_settings()
