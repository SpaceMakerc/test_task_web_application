from small_web.models import CustomUsers


def email_validation(email: str, name: str = None, surname: str = None):
    existed_email = CustomUsers.objects.filter(
        email=email, is_active=True
    ).first()
    if existed_email:
        if not name:
            return True
        if existed_email.name == name and existed_email.surname == surname:
            return False
    return False
