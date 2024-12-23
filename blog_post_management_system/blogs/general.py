from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, BaseFilterBackend
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.views import exception_handler
from rest_framework.views import exception_handler
from http import HTTPStatus
from typing import Any


class MyPaginator(PageNumberPagination):
    """Custom paginator functionality"""

    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "p"

    def get_paginated_response(self, data):
        """
        Customize the response format.
        """
        return Response(
            {
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "total_items": self.page.paginator.count,
                "items_per_page": self.get_page_size(self.request),
                "next_page": self.get_next_link(),
                "previous_page": self.get_previous_link(),
                "results": data,
            }
        )


class MyOrderingFilter(BaseFilterBackend):
    """Custom filter for filtering"""

    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get("ordering", None)
        if ordering:
            descending = ordering.startswith("-")
            ordering_field = ordering.lstrip("-")

            if ordering_field == "total_likes":
                queryset = queryset.annotate(total_likes=Count("likes"))
                ordering_field = "total_likes"

            elif ordering_field == "date_published":
                ordering_field = "date_published"

            else:
                return queryset

            if descending:
                return queryset.order_by(f"-{ordering_field}")
            return queryset.order_by(ordering_field)

        return queryset


def api_exception_handler(exc, context) -> Response:
    """Custom API exception handler."""

    response = exception_handler(exc, context)

    if response is not None:

        http_code_to_message = {
            status.value: status.description for status in HTTPStatus
        }

        error_payload = {
            "error": {
                "status_code": 0,
                "message": "",
                "details": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code

        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data
        response.data = error_payload

    return response
