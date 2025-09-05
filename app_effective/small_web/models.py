from django.db import models

# Create your models here.


class CustomUsers(models.Model):
    """
    Отношение пользователей
    """
    name = models.CharField(
        max_length=50, null=False, verbose_name="Имя"
    )
    surname = models.CharField(
        max_length=50, null=False, verbose_name="Фамилия"
    )
    email = models.EmailField(
        null=False, verbose_name="Почта"
    )
    password = models.BinaryField(
        null=False, verbose_name="Пароль"
    )
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = "custom_users"
        constraints = [
            models.UniqueConstraint(
                fields=("email",), name="unique_email_constraint"
            )
        ]


class AccessTypes(models.Model):
    """
    Отношение типов доступов
    """
    name = models.CharField(max_length=20, primary_key=True)

    class Meta:
        db_table = "access_types"


class UserAccess(models.Model):
    """
    Отношение пользователя и его доступа
    """
    users = models.ForeignKey(
        "CustomUsers", related_name="users", on_delete=models.CASCADE
    )
    access = models.ForeignKey(
        "AccessTypes", related_name="access", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "user_access"


class CustomPermissions(models.Model):
    """
    Отношение типов доступа и пользователей с определением возможных действий
    и кратким описанием
    """
    access_type = models.ForeignKey(
        "AccessTypes", related_name="access_type", on_delete=models.CASCADE
    )
    get = models.BooleanField(default=False)
    post = models.BooleanField(default=False)
    table_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    all_samples = models.BooleanField(default=False)

    class Meta:
        db_table = "custom_permission"
