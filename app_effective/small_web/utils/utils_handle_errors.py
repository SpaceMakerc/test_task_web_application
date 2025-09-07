from django.http import HttpResponseForbidden
from django.template.loader import render_to_string


def get_forbidden_answer():
    answer = render_to_string(
        template_name="exceptions/forbidden_page.html"
    )
    return HttpResponseForbidden(answer)
