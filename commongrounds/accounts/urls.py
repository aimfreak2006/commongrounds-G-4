from django.urls import path

from django.contrib.auth import views
from .views import ProfileUpdateView, RegisterView

app_name = 'accounts'


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("password-reset/", views.PasswordResetView.as_view(
        success_url='/accounts/password-reset/done'
    ), name="password_reset"),
    path("password-reset/done", views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(
        success_url='/accounts/reset/done'
    ), name="password_reset_confirm"),
    path("reset/done", views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path('<str:display_name>/', ProfileUpdateView.as_view(), name='profile_update'),
]
