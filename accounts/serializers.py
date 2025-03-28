from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = serializers.data['password']
        confirm_password = serializers.data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError("Password didn't match")
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name = validated_data['name'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        code = user.generate_verify_code()
        return {
            'message': 'Verification code is sent to your email, please check inbox',
            'code': code
        }
    

class RegisterVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField()


class PasswordResetVerifySerializer(serializers.Serializer):
    code = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        new_password = serializers.data['new_password']
        confirm_password = serializers.data['confirm_password']
        if new_password != confirm_password:
            raise serializers.ValidationError("Password didn't match")
        confirm_password = make_password(confirm_password)
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()