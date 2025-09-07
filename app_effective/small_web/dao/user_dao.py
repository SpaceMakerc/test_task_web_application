from small_web.dao.interface_dao import AbstractDAO
from small_web.models import (
    CustomUsers,
    UserAccess,
    CustomPermissions,
    AccessTypes
)
from small_web.utils.utils_user_auth import get_forbidden_answer


class CustomUserDAO(AbstractDAO):

    def __init__(self, user_info=None, instance=None):
        self.user_email = user_info
        self.table_name = CustomUsers._meta.db_table
        self.instance = instance

    def get_permissions(self):
        user_access = UserAccess.objects.select_related("users").get(
            users__email=self.user_email
        )
        permission = CustomPermissions.objects.filter(
            access_type=user_access.access.name, table_name=self.table_name
        ).first()
        return permission

    def get_sample(self, permission, mark=None):
        """
        Если передан признак определенного пользователя, то получить любого
        пользователя может только user с правами admin, иначе user может
        получить только себя
        Если признак не передан, то получаем информацию в соответствии с правами
        пользователей
        """
        if permission.get:
            if mark:
                mark_samples = CustomUsers.objects.filter(pk=mark)
                if permission.all_samples:
                    return mark_samples
                return mark_samples if mark_samples[0].email == self.user_email\
                    else get_forbidden_answer(
                    context={"error": "Необходимо войти в систему"}
                )

            if permission.all_samples:
                samples = CustomUsers.objects.all()
                return samples
            samples = CustomUsers.objects.filter(email=self.user_email)
            return samples
        raise get_forbidden_answer(
            context={"error": "Необходимо войти в систему"}
        )

    def post_sample(self, permission):
        if permission.post:
            return True
        raise get_forbidden_answer(
            context={"error": "Необходимо войти в систему"}
        )

    def create_access(self):
        access = AccessTypes.objects.get(name="base_user")
        return UserAccess.objects.create(users=self.instance, access=access)
