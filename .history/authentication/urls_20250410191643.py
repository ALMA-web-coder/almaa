from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm, ResetPasswordConfirmForm, ResetPasswordForm

urlpatterns = [
    # Login view with custom login template
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html',
                                                form_class=UserLoginForm,
                                                redirect_authenticated_user=True), name='login'),

    # Logout view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Register view
    path('register/', views.register, name='register'),

    # Activation view
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Password reset view
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html',
                                                                 form_class=ResetPasswordForm), name='password_reset'),

    # Password reset done view
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),

    # Password reset confirm view
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html',
                                                                                                 form_class=ResetPasswordConfirmForm), name='password_reset_confirm'),

    # Password reset complete view
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),

    # Homepage view (if needed)
    path('', views.homepage, name='homepage'),
]