import time

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from blog_user.filter.blog_user_filter import BlogUserFilter
from blog_user.pagination.blog_user_pagination import BlogUserPagination
from blog_user.utils.user_utils import CreateUser, DeleteUser, LaunchUser
from django.db import transaction
from utils.response_msg.server_msg import BLOG_ADMIN_CREATE_USER_ERROR, BLOG_ADMIN_LOGIN_ERROR, \
    BLOG_ADMIN_CREATE_USER_TYPE_ERROR, BLOG_ADMIN_CREATE_USER_GENDER_ERROR, DELETE_USER_ID_ERROR, \
    DELETE_BASE_USER_ID_ERROR, DELETE_USER_ID_COMPARE_ERROR, DELETE_USER_ERROR, DELETE_USER_SELF_ERROR, \
    DATA_TYPE_LIST_ERROR, LAUNCH_BASE_USER_ID_ERROR, LAUNCH_USER_ERROR, LAUNCH_USER_ID_COMPARE_ERROR, \
    LAUNCH_USER_ID_ERROR, DATA_TYPE_DICT_ERROR, EDITOR_USER_ERROR
from rest_framework_jwt.views import ObtainJSONWebToken
from datetime import datetime
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from .models import *
from utils.response_msg.server_msg import BLOG_ADMIN_USER_INFO_ERROR, USER_PERMISSION_LOGIN_ADMIN_REFUSED
from utils.response_data.response import ResponseDate
from utils.permission.admin_permission import AdminPermission
from rest_framework import generics
from blog_user.serializer.blog_user_serializer import BlogUserListSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.db.models.query import QuerySet
from utils.public.get_ip import GetIp
from django.contrib.auth.hashers import make_password

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


# Create your views here.

# admin 登录
class UserLoginAPIView(ObtainJSONWebToken):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(111)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')

            user_id = user.id
            blog_user = BlogUser.objects.filter(base_user_id=user_id).first()

            if not blog_user:
                return ResponseDate.json_data(service_type=BLOG_ADMIN_USER_INFO_ERROR)

            if blog_user.user_type != BlogUser.UserType.super_user.value:
                return ResponseDate.json_data(service_type=USER_PERMISSION_LOGIN_ADMIN_REFUSED)

            response_data = jwt_response_payload_handler(token, user, request)
            response = ResponseDate.json_data(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            blog_user.user_last_login_ip = GetIp.get_login_user_id(request)
            blog_user.user_last_login_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            blog_user.save()
            return response

        return ResponseDate.json_data(service_type=BLOG_ADMIN_LOGIN_ERROR)


# 新增用户
class CreateUserAPIView(APIView):
    """
    创建用户
    """

    permission_classes = [AdminPermission, ]

    @staticmethod
    def post(request):
        create_username = request.data['create_username']
        create_password = request.data['create_password']

        if int(request.data['user_type']) not in BlogUser.USER_TYPE_TEXT.keys():
            return ResponseDate.json_data(service_type=BLOG_ADMIN_CREATE_USER_TYPE_ERROR)

        if int(request.data['user_gender']) not in BlogUser.USER_GENDER_TEXT.keys():
            return ResponseDate.json_data(service_type=BLOG_ADMIN_CREATE_USER_GENDER_ERROR)

        try:
            with transaction.atomic():
                save_id = transaction.savepoint()
                user = CreateUser.create_base_user(
                    create_username, create_password)
                CreateUser.save_user_pic(
                    username=create_username, userid=user.id, request=request)
                transaction.savepoint_commit(save_id)
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(save_id)
            return ResponseDate.json_data(service_type=BLOG_ADMIN_CREATE_USER_ERROR)
        return ResponseDate.json_data()


# 注册用户
class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        pass


# 获取用户列表
class UserListAPIView(generics.ListAPIView):
    serializer_class = BlogUserListSerializer
    permission_classes = [AdminPermission, ]
    queryset = BlogUser.objects.all()
    pagination_class = BlogUserPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = BlogUserFilter

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )
        if self.request.query_params.get('username__icontains'):
            queryset = self.queryset.filter(
                base_user__username__icontains=self.request.query_params['username__icontains'])
        else:
            queryset = self.queryset
        # if isinstance(queryset, QuerySet):
        #     # Ensure queryset is re-evaluated on each request.
        #     queryset = queryset.all()
        return queryset

    def get_fields(self):
        return self.serializer_class.Meta.fields_extra

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        data = {
            'fields': self.get_fields()
        }

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data).data
            data['items'] = result['results']
            data['page'] = {
                'count': result['count']
            }
            return ResponseDate.json_data(data)

        serializer = self.get_serializer(queryset, many=True)

        data = {
            'items': serializer.data,
            'fields': self.get_fields()
        }

        return ResponseDate.json_data(data)

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)


# 删除用户
class UserDeleteAPIView(APIView):
    permission_classes = [AdminPermission, ]
    parser_classes = [JSONParser]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data

        if isinstance(data, list):

            try:
                with transaction.atomic():
                    save_id = transaction.savepoint()
                    for item in data:
                        user = BlogUser.objects.filter(id=item['user_id']).first()

                        if user is None:
                            return ResponseDate.json_data(service_type=DELETE_USER_ID_ERROR)

                        if item['base_user_id'] != user.base_user.id:
                            return ResponseDate.json_data(service_type=DELETE_USER_ID_COMPARE_ERROR)

                        base_user = User.objects.filter(id=item['base_user_id']).first()

                        if base_user is None:
                            return ResponseDate.json_data(service_type=DELETE_BASE_USER_ID_ERROR)

                        if request.user.id == base_user.id:
                            return ResponseDate.json_data(service_type=DELETE_USER_SELF_ERROR)

                        DeleteUser.delete_user(user, base_user)
                    transaction.savepoint_commit(save_id)
            except Exception as e:
                print(e)
                return ResponseDate.json_data(service_type=DELETE_USER_ERROR)

            return ResponseDate.json_data()

        return ResponseDate.json_data(service_type=DATA_TYPE_LIST_ERROR)


# 启用用户
class UserLaunchAPIView(APIView):
    permission_classes = [AdminPermission, ]
    parser_classes = [JSONParser]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data

        if isinstance(data, dict):

            try:
                with transaction.atomic():
                    save_id = transaction.savepoint()
                    user = BlogUser.objects.filter(id=data['user_id']).first()

                    if user is None:
                        return ResponseDate.json_data(service_type=LAUNCH_USER_ID_ERROR)

                    if data['base_user_id'] != user.base_user.id:
                        return ResponseDate.json_data(service_type=LAUNCH_USER_ID_COMPARE_ERROR)

                    base_user = User.objects.filter(id=data['base_user_id']).first()

                    if base_user is None:
                        return ResponseDate.json_data(service_type=LAUNCH_BASE_USER_ID_ERROR)

                    LaunchUser.launch_user(user, base_user)
                    transaction.savepoint_commit(save_id)
            except Exception as e:
                print(e)
                return ResponseDate.json_data(service_type=LAUNCH_USER_ERROR)

            return ResponseDate.json_data()

        return ResponseDate.json_data(service_type=DATA_TYPE_DICT_ERROR)


# 检查用户名是否存在
class CheckUsername(APIView):
    permission_classes = [AdminPermission, ]

    @staticmethod
    def post(request):
        username = request.data.get('username')
        user_id = request.data.get('user_id')

        if user_id is not None:
            username_list = User.objects.exclude(id=user_id).values_list('username', flat=True)
        else:
            username_list = User.objects.all().values_list('username', flat=True)

        if username in username_list:
            data = {
                'check_result': True,
                'msg': '用户名已存在'
            }
            return ResponseDate.json_data(data)

        data = {
            'check_result': False,
            'msg': '用户名不存在'
        }
        return ResponseDate.json_data(data)


class UserEditorAPIView(APIView):
    permission_classes = [AdminPermission, ]

    @staticmethod
    def put(request):
        user_id = request.data['id']
        username = request.data['username']
        base_user = request.data['base_user']
        user_type = request.data['user_type']
        user_phone = request.data.get('user_phone')
        user_email = request.data['user_email']
        user_level = request.data['user_level']
        user_exp = request.data['user_exp']
        user_gender = request.data['user_gender']
        user_birthday = request.data['user_birthday']

        try:
            with transaction.atomic():
                save_id = transaction.savepoint()

                base_user_obj = User.objects.filter(id=base_user).first()
                blog_user_obj = BlogUser.objects.filter(id=user_id).first()
                base_user_obj.username = username
                base_user_obj.save()

                blog_user_obj.user_type = user_type
                blog_user_obj.user_phone = user_phone
                blog_user_obj.user_email = user_email
                blog_user_obj.user_level = user_level
                blog_user_obj.user_exp = user_exp
                blog_user_obj.user_gender = user_gender
                blog_user_obj.user_birthday = user_birthday
                blog_user_obj.save()

                transaction.savepoint_commit(save_id)

        except Exception as e:
            print(e)
            return ResponseDate.json_data(service_type=EDITOR_USER_ERROR)

        return ResponseDate.json_data()


class AddUserAPIView(APIView):
    permission_classes = [AdminPermission, ]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        if int(request.data['user_type']) not in BlogUser.USER_TYPE_TEXT.keys():
            return ResponseDate.json_data(service_type=BLOG_ADMIN_CREATE_USER_TYPE_ERROR)

        if int(request.data['user_gender']) not in BlogUser.USER_GENDER_TEXT.keys():
            return ResponseDate.json_data(service_type=BLOG_ADMIN_CREATE_USER_GENDER_ERROR)

        try:
            with transaction.atomic():
                save_id = transaction.savepoint()
                user = CreateUser.create_base_user(
                    username, password)
                CreateUser.save_user_pic(
                    username=username, userid=user.id, request=request)
                transaction.savepoint_commit(save_id)
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(save_id)
            return ResponseDate.json_data(service_type=BLOG_ADMIN_CREATE_USER_ERROR)
        return ResponseDate.json_data()
