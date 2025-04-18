from django.urls import path
from django.views.generic import TemplateView

from .views import (
    UsersTableView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserChangePasswordView,
    UserSendNewPasswordView,
    TestSendEmailView,
    TestSendWhatsappView
)

app_name = 'user'
urlpatterns = [
    path('', UsersTableView.as_view(), name='table-users'),
    path('create/', UserCreateView.as_view(), name='create-user'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update-user'),
    path('delete/<int:pk>', UserDeleteView.as_view(), name='delete-user'),
    path('send_new_password/<int:pk>', UserSendNewPasswordView.as_view(), name='send-new-password-user'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password-user'),
    path(
        'profile/<int:pk>/',
        TemplateView.as_view(template_name='users/profile.html'),
        name='profile',
    ),
    # path('teste/', TemplateView.as_view(template_name='user/teste.html'), name='teste'),
    path('teste/', TestSendWhatsappView.as_view(), name='teste'),
]
