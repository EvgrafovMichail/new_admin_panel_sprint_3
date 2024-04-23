from django.contrib import admin

from .models import (
    Filmwork,
    Genre,
    GenreFilmwork,
    Person,
    PersonFilmwork,
)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = ("title", "type", "creation_date", "rating")
    list_filter = ("type",)

    search_fields = ("id", "title", "description")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("id", "name", "description")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("id", "full_name")
