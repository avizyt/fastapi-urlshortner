from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    The settings of the application.

    Attributes:
        env_name (str): The name of the environment.
        base_url (str): The base URL of the application.
        db_url (str): The database URL.
    """

    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./urls.db"

    class Config:
        """
        The configuration of the settings.

        Attributes:
            env_file (str): The path to the .env file.
        """

        # create an .env file in the root of the project
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    Get the settings for the application.

    Returns:
        Settings: The settings for the application.
    """
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
