from typing import Any
from dataclasses import (
    dataclass,
    astuple,
    fields,
)

from data_transfering.models.utils import registrate_model


CURRENT_TIMESTAMP = "NOW()"


db_model_mapping = {}


@dataclass(eq=False)
class ContentImmutableBaseModel:
    id: str
    created_at: str

    def as_tuple(self, use_current_time: bool = False) -> tuple[Any]:
        fileds_tuple = astuple(self)

        if use_current_time:
            fileds_tuple = (fileds_tuple[0], CURRENT_TIMESTAMP) + fileds_tuple[2:]

        return fileds_tuple

    def __eq__(self, content: object) -> bool:
        tuple_self = self.as_tuple(use_current_time=True)
        tuple_content = content.as_tuple(use_current_time=True)

        return tuple_self == tuple_content

    @classmethod
    def get_field_names(cls) -> tuple[str]:
        return tuple(field.name for field in fields(cls))


@dataclass(eq=False)
class ContentMutableBaseModel(ContentImmutableBaseModel):
    updated_at: str

    def as_tuple(self, use_current_time: bool = False) -> tuple[Any]:
        fields_tuple = astuple(self)

        if use_current_time:
            fields_tuple = (
                fields_tuple[0],
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
            ) + fields_tuple[3:]

        return fields_tuple


@registrate_model("film_work", db_model_mapping)
@dataclass(eq=False)
class FilmWork(ContentMutableBaseModel):
    title: str
    description: str
    creation_date: str
    file_path: str
    rating: str
    type: str


@registrate_model("genre", db_model_mapping)
@dataclass(eq=False)
class Genre(ContentMutableBaseModel):
    name: str
    description: str


@registrate_model("person", db_model_mapping)
@dataclass(eq=False)
class Person(ContentMutableBaseModel):
    full_name: str


@registrate_model("genre_film_work", db_model_mapping)
@dataclass(eq=False)
class GenreFilmWork(ContentImmutableBaseModel):
    film_work_id: str
    genre_id: str


@registrate_model("person_film_work", db_model_mapping)
@dataclass(eq=False)
class PersonFilmWork(ContentImmutableBaseModel):
    film_work_id: str
    person_id: str
    role: str
