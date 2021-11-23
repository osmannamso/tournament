from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.exceptions import APIException


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    user = serializers.ModelField(User, read_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            raise APIException({
                'password': 'Password or email not correct'
            }, code=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            raise APIException({
                'message': 'User is not active'
            }, code=status.HTTP_400_BAD_REQUEST)
        data.update({
            'user': user
        })

        return data
