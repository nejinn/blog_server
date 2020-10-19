from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginAPIView.as_view()),
    path('create/', CreateUserAPIView.as_view(), name="user create"),
    path('list/', UserListAPIView.as_view()),
    path('delete/', UserDeleteAPIView.as_view()),
    path('launch/', UserLaunchAPIView.as_view()),
    path('check-username/', CheckUsername.as_view()),
    path('editor/', UserEditorAPIView.as_view())
]
