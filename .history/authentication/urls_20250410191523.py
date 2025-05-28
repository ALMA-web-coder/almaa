from django.contrib import admin
from django.urls import path, include
from authentication import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, ResetPasswordForm, ResetPasswordConfirmForm  # Import your forms if needed

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL

    # Include all authentication-related URLs from the authentication app
    path('auth/', include('authentication.urls')),  # This will point to authentication.urls

    # Here, if you need specific views directly defined in this main urls.py, you might want to keep those
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html',
                                                form_class=UserLoginForm,
                                                redirect_authenticated_user=True), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', views.register, name='register'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html',
                                                                 form_class=ResetPasswordForm), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html',
                                                                                                 form_class=ResetPasswordConfirmForm), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),

    path('', views.homepage, name='homepage'),  # Homepage URL
]