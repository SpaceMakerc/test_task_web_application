from rest_framework.exceptions import PermissionDenied


def get_forbidden_answer():
    return PermissionDenied()
