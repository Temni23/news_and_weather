import base64

from django.contrib.auth.hashers import make_password
from django.core import validators
from django.core.files.base import ContentFile
from rest_framework import serializers

from news.models import Publication
from news_and_weather.settings import (MAX_LENGTH_USERNAME, MAX_LENGTH_EMAIL,
                                       MAX_LENGTH_FIRST_NAME,
                                       MAX_LENGTH_LAST_NAME)
from users.models import User


class Base64ImageField(serializers.ImageField):
    """Сериалайзер используется для изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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


class PublicationSerializer(serializers.ModelSerializer):
    main_image = Base64ImageField(required=True, allow_null=False)

    # TODO поле не отображается обязательным в сваггере

    class Meta:
        model = Publication
        fields = ('id', 'title', 'text', 'main_image', 'preview_image', 'text',
                  'date_published', 'author')
        read_only_fields = ('pub_date', 'author')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        publication = Publication.objects.create(**validated_data)
        return publication
