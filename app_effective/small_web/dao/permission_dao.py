from small_web.dao.interface_dao import AbstractDAO
from small_web.models import CustomPermissions, UserAccess
from small_web.utils.utils_user_auth import get_forbidden_answer


class CustomPermissionDAO(AbstractDAO):

    def __init__(self, user_info):
        self.user_email = user_info
        self.table_name = CustomPermissions._meta.db_table

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
        Так как только user  правами admin может посещать страницу, то всегда
        отдаём все записси
        """
        if permission.get:
            if mark:
                samples = CustomPermissions.objects.filter(pk=mark)
                return samples
            samples = CustomPermissions.objects.all()
            return samples
        return get_forbidden_answer()

    def post_sample(self, permission):
        if permission.post:
            return True
        raise get_forbidden_answer()

