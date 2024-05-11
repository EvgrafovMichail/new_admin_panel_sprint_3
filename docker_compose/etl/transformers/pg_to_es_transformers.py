from typing import Any

from psycopg2.extras import DictRow
from pydantic import BaseModel

from transformers.enumerations import Roles
from transformers.shemas_es import (
    FilmWorkRecordES,
    PersonRecordES,
)


class TransformerPG2ESGeneral:
    _es_scheme: BaseModel

    def __init__(self, es_scheme: BaseModel) -> None:
        self._es_scheme = es_scheme

    def __call__(self, data_pg: list[DictRow]) -> list[dict[str, Any]]:
        return [
            self._es_scheme(**dict(data_frame)).model_dump() for data_frame in data_pg
        ]


class TransformPG2ESFilmwork:
    def __call__(self, data_pg: list[DictRow]) -> list[dict[str, Any]]:
        data_es = []

        for data_frame in data_pg:
            persons = data_frame["persons"]
            director_names, directors = self._group_persons_by_roles(
                persons, Roles.DIRECTOR
            )
            writer_names, writers = self._group_persons_by_roles(persons, Roles.WRITER)
            actor_names, actors = self._group_persons_by_roles(persons, Roles.ACTOR)

            data_frame_es = FilmWorkRecordES(
                id=data_frame["id"],
                title=data_frame["title"],
                description=data_frame["description"],
                imdb_rating=data_frame["rating"],
                genres=data_frame["genres"],
                directors_names=director_names,
                actors_names=actor_names,
                writers_names=writer_names,
                directors=directors,
                actors=actors,
                writers=writers,
            )
            data_es.append(data_frame_es.model_dump())

        return data_es

    @staticmethod
    def _group_persons_by_roles(
        persons: list[DictRow], role: str
    ) -> tuple[list[str], list[PersonRecordES]]:
        role = Roles(role)
        person_names, person_info = [], []
        person_name_key = "person_name"

        for person in persons:
            person_role = Roles(person["person_role"])

            if person_role != role:
                continue

            person_names.append(person[person_name_key])
            person_info.append(
                PersonRecordES(
                    person_id=person["person_id"],
                    person_name=person[person_name_key],
                )
            )

        return person_names, person_info
