from django.urls import path
from .views import CreateUserAPIView, UserLoginAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view()),
    path('create/', CreateUserAPIView.as_view(), name="user create")
]
