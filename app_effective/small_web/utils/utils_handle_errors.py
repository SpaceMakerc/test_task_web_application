from rest_framework.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework import status


def get_forbidden_answer():
    return PermissionDenied()


def get_unauthorized_answer():
    answer = render_to_string(
        template_name="exceptions/unauthorized.html"
    )
    return HttpResponse(answer, status=status.HTTP_401_UNAUTHORIZED)

