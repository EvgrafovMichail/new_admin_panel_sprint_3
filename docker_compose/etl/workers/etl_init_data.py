from extractors.sql_queries import (
    QUERY_FILM_WORK_FILM_WORK,
    QUERY_FILM_WORK_PERSON,
    QUERY_FILM_WORK_GENRE,
    QUERY_PERSON,
    QUERY_GENRE,
)

from transformers.pg_to_es_transformers import (
    TransformerPG2ESGeneral,
    TransformPG2ESFilmwork,
)
from transformers.shemas_es import (
    PersonRecordES,
    GenreRecordES,
)


query_transformer_index = [
    (QUERY_FILM_WORK_FILM_WORK, TransformPG2ESFilmwork(), "movies"),
    (QUERY_FILM_WORK_PERSON, TransformPG2ESFilmwork(), "movies"),
    (QUERY_FILM_WORK_GENRE, TransformPG2ESFilmwork(), "movies"),
    (QUERY_PERSON, TransformerPG2ESGeneral(PersonRecordES), "persons"),
    (QUERY_GENRE, TransformerPG2ESGeneral(GenreRecordES), "genres"),
]
