from rest_framework import serializers

from small_web.models import CustomUsers


class CustomUsersSerializer(serializers.ModelSerializer):
    # def validate_email(self):

    class Meta:
        model = CustomUsers
        fields = ("name", "surname", "email", "password")
