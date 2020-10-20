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


class BlogUserListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='base_user.username')
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user_last_login_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # gender = serializers.SerializerMethodField(label='用户性别')
    create_user = serializers.SerializerMethodField(label='创建人')
    update_user = serializers.SerializerMethodField(label='更新人')

    class Meta:
        model = BlogUser
        fields = [
            'username',
            'base_user',
            'id',
            'user_pic',
            'user_type',
            'user_phone',
            'user_email',
            'user_exp',
            'user_level',
            'user_last_login_time',
            'user_birthday',
            'user_gender',
            'create_date',
            'update_date',
            'is_delete',
            'create_user',
            'update_user',
            'user_ip',
            'user_last_login_ip',
        ]
        fields_extra = [
            {
                'key': "isSelected",
                'label': "选中",
                'class': "text-center text-info",
                'stickyColumn': True

            },
            {
                'key': 'user_pic',
                'label': "头像",
                'class': "text-center",
                'stickyColumn': True
            },
            {
                'key': 'base_user',
                'label': "用户ID",
                'class': "text-center",
                'stickyColumn': True
            },
            {
                'key': 'username',
                'label': "用户名",
                'class': "text-center",
                'stickyColumn': True
            },
            {
                'key': 'id',
                'label': "用户资料ID",
                'class': "text-center"
            },
            {
                'key': 'user_type',
                'label': "用户类型",
                'class': "text-center"
            },
            {
                'key': 'user_phone',
                'label': "用户电话",
                'class': "text-center"
            },
            {
                'key': 'user_email',
                'label': "用户邮箱",
                'class': "text-center"
            },
            {
                'key': 'user_exp',
                'label': "用户经验值",
                'class': "text-center"
            },
            {
                'key': 'user_level',
                'label': "用户等级",
                'class': "text-center"
            },
            {
                'key': 'user_last_login_time',
                'label': "最近登录时间",
                'class': "text-center"
            },
            {
                'key': 'user_birthday',
                'label': "用户生日",
                'class': "text-center"
            },
            {
                'key': 'user_gender',
                'label': "用户性别",
                'class': "text-center"
            },
            {
                'key': 'user_ip',
                'label': "注冊ip",
                'class': "text-center"
            },
            {
                'key': 'user_last_login_ip',
                'label': "最近登录ip",
                'class': "text-center"
            },
            {
                'key': 'create_date',
                'label': "创建日期",
                'class': "text-center"
            },
            {
                'key': 'update_date',
                'label': "更新日期",
                'class': "text-center"
            },
            {
                'key': 'is_delete',
                'label': "是否停用",
                'class': "text-center"
            },
            {
                'key': 'create_user',
                'label': "创建人",
                'class': "text-center"
            },
            {
                'key': 'update_user',
                'label': "更新人",
                'class': "text-center"
            },
            {
                'key': "action",
                'label': "操作",
                'class': "text-center"
            }
        ]

    # @staticmethod
    # def get_gender(obj):
    #     """
    #     固定写法,obj代表实例对象
    #     """
    #     gender = obj.user_gender
    #     return obj.USER_GENDER_TEXT[gender]

    @staticmethod
    def get_create_user(obj):
        create_id = obj.create_id
        create_user = User.objects.filter(id=create_id).first().username
        return create_user

    @staticmethod
    def get_update_user(obj):
        update_id = obj.create_id
        update_user = User.objects.filter(id=update_id).first().username
        return update_user
