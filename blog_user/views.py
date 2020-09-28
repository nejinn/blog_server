from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from blog_user.utils.create_user import CreateUser
from django.db import transaction
from utils.response_data.response import ResponseDate
from utils.response_msg.server_msg import BLOG_ADMIN_CREATE_USER_ERROR, BLOG_ADMIN_LOGIN_ERROR
from rest_framework.response import Serializer
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


# Create your views here.

class UserLoginAPIView(ObtainJSONWebToken):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = ResponseDate.json_data(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return ResponseDate.json_data(service_type=BLOG_ADMIN_LOGIN_ERROR)


class CreateUserAPIView(APIView):
    """
    创建用户
    """

    @staticmethod
    def post(request):
        create_username = request.data['create_username']
        create_password = request.data['create_password']

        try:
            with transaction.atomic():
                save_id = transaction.savepoint()
                user = CreateUser.create_base_user(
                    create_username, create_password)
                CreateUser.save_user_pic(
                    username=create_username, userid=user.id)
                transaction.savepoint_commit(save_id)
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(save_id)
            return ResponseDate.json_data(service_type=BLOG_ADMIN_CREATE_USER_ERROR)
        return ResponseDate.json_data()


class RegisterUserAPIView(APIView):

    permission_classes = [AllowAny, ]

    def post(request):
        pass
