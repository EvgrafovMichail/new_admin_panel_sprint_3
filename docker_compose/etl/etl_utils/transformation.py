from typing import Any

from psycopg2.extras import DictRow

from etl_utils.enumerations import (
    PersonKeys,
    Roles,
)
from etl_utils.shemas import (
    FilmWorkInfo,
    PersonInfo,
)


def group_person_by_roles(
    persons: list[dict[str, str]],
    role: str,
) -> tuple[list[str], list[PersonInfo]]:
    role = Roles(role)

    person_names, person_info = [], []

    for person in persons:
        if Roles(person[PersonKeys.ROLE.value]) != role:
            continue

        person_names.append(person[PersonKeys.NAME.value])
        person_info.append(
            PersonInfo(
                id=person[PersonKeys.ID.value],
                name=person[PersonKeys.NAME.value],
            )
        )

    return person_names, person_info


def transform_sql_data(data: list[DictRow]) -> list[dict[str, Any]]:
    data_transformed = []

    for data_row in data:
        persons = data_row["persons"]
        director_names, directors = group_person_by_roles(
            persons, Roles.DIRECTOR
        )
        actor_names, actors = group_person_by_roles(persons, Roles.ACTOR)
        writer_names, writers = group_person_by_roles(persons, Roles.WRITER)

        data_model = FilmWorkInfo(
            id=data_row["id"],
            title=data_row["title"],
            description=data_row["description"],
            imdb_rating=data_row["rating"],
            genres=data_row["genres"],
            directors_names=director_names,
            actors_names=actor_names,
            writers_names=writer_names,
            directors=directors,
            actors=actors,
            writers=writers,
        )

        data_transformed.append(data_model.model_dump())

    return data_transformed
