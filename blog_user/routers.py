from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import CreateUserAPIView

urlpatterns = [
    path('user/login/', obtain_jwt_token),
    path('user/create/', CreateUserAPIView.as_view(), name="user create")
]
