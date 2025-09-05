from small_web.dao.interface_dao import AbstractDAO
from small_web.models import CustomUsers, UserAccess, CustomPermissions
from small_web.utils.utils_user_auth import get_forbidden_answer


class CustomUserDAO(AbstractDAO):

    def __init__(self, user_info):
        self.user_email = user_info
        self.table_name = CustomUsers._meta.db_table

    def get_permissions(self):
        user_access = UserAccess.objects.select_related("users").get(
            users__email=self.user_email
        )
        permission = CustomPermissions.objects.filter(
            access_type=user_access.access.name, table_name=self.table_name
        ).first()
        return permission

    def get_sample(self, permission):
        if permission.get:
            if permission.all_samples:
                samples = CustomUsers.objects.all()
                return samples
            samples = CustomUsers.objects.filter(email=self.user_email)
            return samples
        raise get_forbidden_answer()

    def post_sample(self, permission):
        ...

