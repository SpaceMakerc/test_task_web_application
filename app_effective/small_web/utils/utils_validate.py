from small_web.models import CustomUsers


def email_validation_on_creating(email: str):
    existed_email = CustomUsers.objects.filter(
        email=email, is_active=True
    ).first()
    return False if not existed_email else True


def email_validation_on_updating(
        new_email: str,
        user_id: str
):
    row_from_db_by_new_email = CustomUsers.objects.filter(
        email=new_email, is_active=True
    ).first()
    if row_from_db_by_new_email:
        user_info_by_id = CustomUsers.objects.filter(pk=user_id).first()
        if row_from_db_by_new_email.email == user_info_by_id.email:
            return new_email
        return None
    return new_email
