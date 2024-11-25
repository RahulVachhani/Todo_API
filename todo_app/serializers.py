from rest_framework import serializers
from .models import Todo

from django.contrib.auth.models import User

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

        def validate(self,data):
            if not data:
                raise serializers.ValidationError('Please enter the data')

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username= data['username']).exists():
                raise serializers.ValidationError('Username already taken')
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'], password = validated_data['password'])

        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    
