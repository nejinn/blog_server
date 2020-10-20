import django_filters
from blog_user.models import *


class BlogUserFilter(django_filters.FilterSet):

    class Meta:
        model = BlogUser
        fields = {
            'user_type': ['exact'],
            'user_phone': ['icontains'],
            'user_email': ['icontains'],
            'is_delete': ['exact']
        }
