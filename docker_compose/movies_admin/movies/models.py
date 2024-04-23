import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(
        _("name"),
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_("full_name"), blank=False, null=False)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

    def __str__(self) -> str:
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkTypes(models.TextChoices):
        MOVIE = "movie"
        TV_SHOW = "tv_show"

    title = models.TextField(_("title"), blank=False, null=False)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    type = models.TextField(_("type"), choices=FilmworkTypes.choices)
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"

        indexes = [
            models.Index(fields=["creation_date"], name="film_work_creation_date_idx")
        ]

    def __str__(self) -> str:
        return self.title


class GenreFilmwork(UUIDMixin):
    genre_id = models.ForeignKey(
        "Genre",
        on_delete=models.CASCADE,
        db_column="genre_id",
    )
    film_work_id = models.ForeignKey(
        "Filmwork",
        on_delete=models.CASCADE,
        db_column="film_work_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = "Жанр фильма"
        verbose_name_plural = "Жанры фильмa"

        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "genre_id"],
                name="film_work_genre_idx",
            )
        ]


class PersonFilmwork(UUIDMixin):
    class RoleTypes(models.TextChoices):
        DIRECTOR = "director"
        ACTOR = "actor"
        WRITER = "writer"

    film_work_id = models.ForeignKey(
        "Filmwork",
        on_delete=models.CASCADE,
        db_column="film_work_id",
    )
    person_id = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        db_column="person_id",
    )
    role = models.TextField(
        _("role"),
        choices=RoleTypes.choices,
        blank=False,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = "Роль персоны"
        verbose_name_plural = "Роли персоны"

        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_idx",
            )
        ]
