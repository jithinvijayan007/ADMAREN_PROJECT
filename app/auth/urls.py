from django.urls import path
from app.auth.views import RegistrationView, UserLoginView, LogoutAPIView

urlpatterns = [
    path('register/',RegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout")
]