from typing import Any

from django.contrib.postgres.aggregates import ArrayAgg
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.db.models.functions import Cast
from django.db.models import TextField, Q
from django.http import JsonResponse


from movies.models import (
    Filmwork,
    PersonFilmwork,
)


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = (
            Filmwork.objects.all()
            .values("title", "description", "creation_date", "rating", "type")
            .annotate(id=Cast("id", output_field=TextField()))
            .annotate(genres=ArrayAgg("genres__name", distinct=True))
            .annotate(
                actors=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.ACTOR),
                ),
            )
            .annotate(
                directors=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.DIRECTOR),
                )
            )
            .annotate(
                writers=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.WRITER),
                )
            )
        )
        return queryset

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs
    ) -> JsonResponse:
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, **_) -> dict[str, Any]:
        queryset = self.get_queryset()
        paginator, _, _, _ = self.paginate_queryset(
            queryset, page_size=self.paginate_by
        )

        if (page_id := self.request.GET.get("page", 1)) == "last":
            page_id = paginator.num_pages

        page_id = int(page_id)
        page = paginator.page(page_id)

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page_id - 1 if page.has_previous() else None,
            "next": page_id + 1 if page.has_next() else None,
            "results": list(page),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    pk_url_kwarg = "id"

    def get_context_data(self, **_) -> dict[str, Any]:
        queryset = self.get_queryset()
        filmwork_id = str(self.kwargs["id"])

        filmwork_record = queryset.filter(id=filmwork_id)
        context = list(filmwork_record)[0]

        return context
