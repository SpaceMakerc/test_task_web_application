from rest_framework import serializers

from small_web.models import CustomUsers
from small_web.utils.utils_password import modify_password


class CustomUsersSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        error_messages={"blank": "Поле пароль не может быть пустым"},
        label="Пароль"
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        error_messages={"blank": "Поле Пароль не может быть пустым"},
        label="Повторите пароль",
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password": "Значения паролей должны быть одинаковыми"
            })
        attrs["password"] = modify_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        del validated_data["password2"]
        return CustomUsers.objects.create(**validated_data)

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


class CustomUsersSignInSerializer(serializers.Serializer):
    email = serializers.EmailField(
        allow_null=False,
        error_messages={"blank": "Поле Почта не может быть пустым"},
        label="Почта"
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        error_messages={"blank": "Поле пароль не может быть пустым"},
        label="Пароль"
    )

    class Meta:
        fields = ("email", "password")
