from django.db import models

# Create your models here.


class CustomUsers(models.Model):
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False)
    password = models.CharField(null=False)

    class Meta:
        db_table = "custom_users"
