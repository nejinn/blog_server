from django.urls import path
from .views import CreateUserAPIView, UserLoginAPIView

urlpatterns = [
    path('user/login/', UserLoginAPIView.as_view()),
    path('user/create/', CreateUserAPIView.as_view(), name="user create")
]
