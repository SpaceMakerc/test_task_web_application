from rest_framework import serializers

from small_web.models import CustomUsers


class CustomUsersSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        error_messages={"blank": "Поле пароль не может быть пустым"},
        label="Пароль"
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        error_messages={"blank": "Поле пароль не может быть пустым"},
        label="Повторите пароль",
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                "Значения паролей должны быть одинаковыми"
            )
        return attrs

    class Meta:
        model = CustomUsers
        fields = ("name", "surname", "email", "password", "password2")
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "Поле Имя не может быть пустым",
                },
            },
            "surname": {
                "error_messages": {
                    "blank": "Поле Фамилия не может быть пустым",
                },
            },
            "email": {
                "error_messages": {
                    "blank": "Поле Почта не может быть пустым",
                },
            },
        }
