from django.urls import path, include
from django.contrib.auth import views as auth_views
from authentication import views
from authentication.forms import UserLoginForm, ResetPasswordConfirmForm, ResetPasswordForm
from .views import application_view,  track_application
from django.views.generic import TemplateView  


urlpatterns = [
   path('login/', views.login_view, name='login'),


    # logout view from auth_view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path for register view
    path('register/', views.register, name='register'),

    #path for activate view
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    #path to reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html',
                                                                 form_class=ResetPasswordForm), name='password_reset'),

    #path to password_reset_done
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),

    #path to password_reset_confirm
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html',
                                                                                                 form_class=ResetPasswordConfirmForm), name='password_reset_confirm'),

    #path to password reset complete
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),


    # path for homepage where successfull login will redirect
    path('', views.homepage, name='homepage'),
    
    
    path('applications/', views.application_list, name='application_list'),  
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),
     path('apply/', application_view, name='application_view'), 
    path('apply/success/', TemplateView.as_view(template_name='application/success.html'), name='application_success'),  
    path('track/', track_application, name='track_application')
    
    path('applications/<int:application_id>/', registrar_view, name='registrar_view'),



]