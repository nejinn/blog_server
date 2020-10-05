from django.urls import path
from .views import UserInfoAPIView

urlpatterns = [
    path('user_info/', UserInfoAPIView.as_view()),
]
