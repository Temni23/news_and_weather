from django.contrib.auth.hashers import make_password
from django.core import validators
from rest_framework import serializers

from news_and_weather.settings import (MAX_LENGTH_USERNAME, MAX_LENGTH_EMAIL,
                                       MAX_LENGTH_FIRST_NAME,
                                       MAX_LENGTH_LAST_NAME)
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер используется для отображения с пользователя."""
    id = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'role')
        model = User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер используется для создания пользователя."""
    username = serializers.CharField(max_length=MAX_LENGTH_USERNAME,
                                     required=True,
                                     validators=(
                                         validators.MaxLengthValidator(
                                             MAX_LENGTH_USERNAME),
                                         validators.RegexValidator(
                                             r'^[\w.@+-]+\Z')
                                     ))
    first_name = serializers.CharField(max_length=MAX_LENGTH_FIRST_NAME,
                                       required=True,
                                       validators=(
                                           validators.MaxLengthValidator(
                                               MAX_LENGTH_FIRST_NAME),
                                       ))
    last_name = serializers.CharField(max_length=MAX_LENGTH_LAST_NAME,
                                      required=True,
                                      validators=(
                                          validators.MaxLengthValidator(
                                              MAX_LENGTH_LAST_NAME),
                                      ))
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL,
                                   required=True)
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',
                  'password')

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get('email'))
        if user:
            user = user.first()
            if user.username != attrs.get('username'):
                raise serializers.ValidationError(
                    {'Этот email уже используется другим пользователем'}
                )
        user = User.objects.filter(username=attrs.get('username')).first()
        if user:
            if user.email != attrs.get('email'):
                raise serializers.ValidationError(
                    {'Это имя пользователя уже используется'}
                )
        if attrs.get('password'):
            attrs['password'] = make_password(attrs['password'])
        return super().validate(attrs)
