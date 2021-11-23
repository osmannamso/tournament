from django.urls import path

from userinfo.views import UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view()),
]
