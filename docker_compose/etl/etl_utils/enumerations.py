from enum import Enum


class Roles(Enum):
    DIRECTOR = "director"
    ACTOR = "actor"
    WRITER = "writer"


class PersonKeys(Enum):
    ID = "person_id"
    NAME = "person_name"
    ROLE = "person_role"
