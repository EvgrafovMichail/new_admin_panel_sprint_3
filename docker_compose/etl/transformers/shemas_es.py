from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GenreRecordES(BaseModel):
    id: UUID
    name: str = Field(max_length=255)
    description: Optional[str] = None


class PersonRecordES(BaseModel):
    id: UUID = Field(alias="person_id")
    name: str = Field(alias="person_name")


class FilmWorkRecordES(BaseModel):
    id: UUID
    title: str
    description: str | None
    imdb_rating: float | None
    genres: list[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[PersonRecordES]
    actors: list[PersonRecordES]
    writers: list[PersonRecordES]
