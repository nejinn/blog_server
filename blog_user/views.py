from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from blog_user.utils.create_user import CreateUser
from django.db import transaction
from utils.response_data.response import ResponseDate
from utils.response_msg.server_msg import BLOG_ADMIN_CREATE_USER_ERROR
from rest_framework.response import Serializer


# Create your views here.

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
                user = CreateUser.create_base_user(create_username, create_password)
                CreateUser.save_user_pic(username=create_username, userid=user.id)
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
