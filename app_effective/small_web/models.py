from django.db import models

# Create your models here.


class CustomUsers(models.Model):
    name = models.CharField(
        max_length=50, null=False, verbose_name="Имя"
    )
    surname = models.CharField(
        max_length=50, null=False, verbose_name="Фамилия"
    )
    email = models.EmailField(
        null=False, verbose_name="Почта", unique=True
    )
    password = models.BinaryField(
        null=False, verbose_name="Пароль"
    )

    class Meta:
        db_table = "custom_users"
