from rest_framework import serializers
from blog_user.models import *


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class BlogUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='base_user.username')
    create_date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = BlogUser
        fields = [
            'username',
            'base_user',
            'user_pic',
            'user_type',
            'user_phone',
            'user_email',
            'user_exp',
            'user_level',
            'user_birthday',
            'user_gender',
            'create_date'
        ]
