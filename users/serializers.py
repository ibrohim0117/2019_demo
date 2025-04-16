from django.contrib.auth.hashers import make_password
from rest_framework.serializers import Serializer, ModelSerializer
from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


class UserCreateSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'password']

    def validate_password(self, value):
        value = make_password(value)
        return value

    def to_representation(self, instance):
        pass


class UserLoginSerializer(TokenObtainSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError("Bunday email mavjud emas")

        auth_user = authenticate(email=email, password=password)
        # print(auth_user)
        if not auth_user:
            raise ValidationError("Email yoki parol xato")

        data = {
            'access_token': auth_user.token()['access_token'],
            'refresh_token': auth_user.token()['refresh_token'],
        }

        return data


class UserUpdateSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    new_password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'phone', 'new_password', 'old_password']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        old_password = attrs.get('old_password')
        if new_password != old_password:
            raise ValidationError("Parol xato")
        return attrs

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.password = make_password(validated_data.get('new_password', instance.password))
        instance.save()
        return instance


