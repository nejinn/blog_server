from django.urls import path
from .views import UserInfoAPIView

urlpatterns = [
    path('user-info/', UserInfoAPIView.as_view()),
]
