from utils.response_data.response import ResponseDate
from .models import Sidebar
from utils.recursion_data.recursion_sidebar import RecursionSidebar
from blog_user.serializer.blog_user_serializer import BlogUserSerializer
from rest_framework import generics
from blog_user.models import BlogUser
from utils.response_msg.server_msg import BLOG_ADMIN_USER_INFO_ERROR
from utils.permission.admin_permission import AdminPermission


# Create your views here.


class UserInfoAPIView(generics.GenericAPIView):
    serializer_class = BlogUserSerializer
    queryset = BlogUser.objects.all()
    permission_classes = [AdminPermission, ]

    def get(self, request):
        sidebar_all = list(
            Sidebar.objects.filter(
                is_delete=False
            ).order_by(
                'order'
            ).values(
                'order',
                'name',
                'level',
                'parent',
                'id',
                'icon',
                'router',
                'active'
            )
        )

        sidebar = RecursionSidebar.x_tree(sidebar_all)

        blog_user_queryset = BlogUser.objects.filter(base_user_id=request.user.id).first()

        if not blog_user_queryset:
            return ResponseDate.json_data(service_type=BLOG_ADMIN_USER_INFO_ERROR)

        self.get_serializer()

        data = {
            'user_sidebar': sidebar,
            'user_info': self.get_serializer(instance=blog_user_queryset).data
        }

        return ResponseDate.json_data(data)
