from rest_framework import serializers

from small_web.models import CustomUsers, CustomPermissions, AccessTypes
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
        existed_email = CustomUsers.objects.filter(
            email=attrs["email"], is_active=True
        ).exists()
        if existed_email:
            raise serializers.ValidationError({
                "email": "Пользователь с такой почтой уже существует"
            })

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


class CustomUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ("id", "name", "surname", "email")


class CustomSerializerUpdateInfoSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

    class Meta:
        model = CustomUsers
        fields = ("name", "surname", "email")
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


class CustomPermissionSerializer(serializers.ModelSerializer):

    def validate_access_type(self, value):
        available_permissions = AccessTypes.objects.all()
        if not any(
                value == access.name for access in available_permissions
        ):
            raise serializers.ValidationError("Несуществующий тип доступа")
        return value

    def update(self, instance, validated_data):
        instance.id = validated_data.get(
            'id', instance.id
        )
        instance.get = validated_data.get(
            'get', instance.get
        )
        instance.post = validated_data.get(
            'post', instance.post
        )
        instance.table_name = validated_data.get(
            'table_name', instance.table_name
        )
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.all_samples = validated_data.get(
            'all_samples', instance.all_samples
        )
        instance.access_type = self.get_access_type(
            validated_data.get('access_type'), instance.access_type
        )
        instance.save()
        return instance

    def get_access_type(self, access, old_access):
        new_access = None
        if access:
            new_access = AccessTypes.objects.filter(name=access).first()
        return new_access if new_access else old_access

    get = serializers.BooleanField(
        allow_null=False,
        error_messages={"blank": "Поле GET не может быть пустым"},
        label="Метод GET"
    )
    post = serializers.BooleanField(
        allow_null=False,
        error_messages={"blank": "Поле POST не может быть пустым"},
        label="Метод POST"
    )
    table_name = serializers.CharField(
        allow_null=False,
        error_messages={"blank": "Поле Название таблицы не может быть пустым"},
        label="Название таблицы"
    )
    description = serializers.CharField(
        allow_null=False,
        error_messages={"blank": "Поле Описание таблицы не может быть пустым"},
        label="Описание"
    )
    all_samples = serializers.BooleanField(
        allow_null=False,
        error_messages={
            "blank": "Поле Показа экземпляров таблицы не может быть пустым"
        },
        label="Показать все экземпляры"
    )
    access_type = serializers.CharField(
        allow_null=False,
        error_messages={
            "blank": "Поле Тип доступа не может быть пустым"
        },
        label="Тип доступа ('base_user' - обычный пользователь, 'admin' - "
              "пользователь с повышенными правами)"
    )

    class Meta:
        model = CustomPermissions
        fields = (
            "id", "get", "post", "table_name",
            "description", "all_samples", "access_type"
        )
        extra_kwargs = {
            "id": {
                "error_messages": {
                    "blank": "Поле ID не может быть пустым",
                },
            }
        }
