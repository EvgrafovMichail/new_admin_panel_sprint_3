from pydantic_settings import BaseSettings
from pydantic import AliasChoices, Field


class DataBaseSettings(BaseSettings):
    dbname: str = Field(validation_alias=AliasChoices("DB_NAME"))
    user: str = Field(validation_alias=AliasChoices("DB_USER"))
    password: str = Field(validation_alias=AliasChoices("DB_PASSWORD"))
    host: str = Field(validation_alias=AliasChoices("DB_HOST"))
    port: int = Field(
        validation_alias=AliasChoices("DB_PORT"),
        gt=0,
        default=5432,
    )
    options: str = Field(
        validation_alias=AliasChoices("DB_OPTIONS"),
        default="-c search_path=public,content",
    )


class ElasticSearchSettings(BaseSettings):
    host: str = Field(validation_alias=AliasChoices("ELASTIC_HOST"))
    port: int = Field(
        validation_alias=AliasChoices("ELASTIC_PORT"),
        gt=0,
        default=9200,
    )
