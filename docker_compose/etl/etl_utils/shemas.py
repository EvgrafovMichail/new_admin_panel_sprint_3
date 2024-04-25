from uuid import UUID

from pydantic import BaseModel


class PersonInfo(BaseModel):
    id: UUID
    name: str


class FilmWorkInfo(BaseModel):
    id: UUID
    title: str
    description: str | None
    imdb_rating: float | None
    genres: list[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[PersonInfo]
    actors: list[PersonInfo]
    writers: list[PersonInfo]
