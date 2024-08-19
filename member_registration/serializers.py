from django.contrib.auth.models import User
from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User 
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            username = validated_data['username']
        )
    
        user.set_password(validated_data['password'])
        user.save()

        return user 
    

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    token = serializers.CharField()


class MemberDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username', 'email', 'password')