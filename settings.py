from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str = "my_awesome_secret"
    static_dir = "static"
    static_url = "/static"


settings = Settings()
