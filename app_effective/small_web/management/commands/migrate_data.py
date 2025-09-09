from django.core.management.base import BaseCommand

from small_web.models import (
    CustomUsers,
    AccessTypes,
    UserAccess,
    CustomPermissions
)
from small_web.utils.utils_password import modify_password


class Command(BaseCommand):
    help = "Добавление информацию в БД"

    def handle(self, *args, **options):
        # Создание CustomUsers
        user = CustomUsers.objects.create(
            name="test_user",
            surname="user_test",
            email="test_user@mail.ru",
            password=modify_password("12345qwerty")  # Пароль для test_user
        )
        user_admin = CustomUsers.objects.create(
            name="admin_test_user",
            surname="admin_test",
            email="test_admin@mail.ru",
            password=modify_password("qwerty12345"),  # Пароль для admin_test_user
            is_admin=True
        )

        # Создание типов доступа
        access1 = AccessTypes.objects.create(name="base_user")
        access2 = AccessTypes.objects.create(name="admin")
        
        # Выставление прав пользователям
        UserAccess.objects.create(users=user, access=access1)
        UserAccess.objects.create(users=user_admin, access=access2)

        # Описание прав доступа
        permissions = [
            CustomPermissions(
                get=True,
                post=True,
                table_name="custom_users",
                description="Может просматривать и изменять только свой экземпляр CustomUsers",
                access_type=access1,
                all_samples=False
            ),
            CustomPermissions(
                get=True,
                post=True,
                table_name="custom_users",
                description="Может просматривать и изменять любой экземпляр CustomUsers",
                access_type=access2,
                all_samples=True
            ),
            CustomPermissions(
                get=True,
                post=True,
                table_name="custom_permission",
                description="Может просматривать и вносить изменения во все экземпляры CustomPermissions",
                access_type=access2,
                all_samples=True
            ),
            CustomPermissions(
                get=False,
                post=False,
                table_name="custom_permission",
                description="Нет доступа на просмотр и внесения информации в экземпляры CustomPermissions",
                access_type=access1,
                all_samples=False
            )
        ]

        CustomPermissions.objects.bulk_create(permissions)
