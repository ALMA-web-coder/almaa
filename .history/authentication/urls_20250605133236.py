from django.urls import path, include
from django.contrib.auth import views as auth_views
from authentication import views
from authentication.forms import UserLoginForm, ResetPasswordConfirmForm, ResetPasswordForm
from .views import masters_application, certificate_application
from .views import  form_complete, payment_cancelled
from django.views.generic import TemplateView  
from authentication.views import PrivacyPolicyView
from .views import download_pdf, download_word, download_excel
from .views import general_payment, payment_timeout


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='authentication/password_reset.html',
        form_class=ResetPasswordForm
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='authentication/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/password_reset_confirm.html',
        form_class=ResetPasswordConfirmForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='authentication/password_reset_complete.html'
    ), name='password_reset_complete'),
    
  
    path('track_application/', views.track_application, name='track_application'),

    # path for homepage where successfull login will redirect
    path('homepage/', views.homepage, name='homepage'),
    
    
    path('applications/', views.application_list, name='application_list'),  
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),

    path('track/', views.track_application, name='track_application'),
    
    path('applications/<int:application_id>/', views.registrar_view, name='registrar_view'),
     path('masters-application/', masters_application, name='masters_application'),
    path('certificate-application/', certificate_application, name='certificate_application'),
   
    path('application/<int:application_id>/download/pdf/', views.download_pdf, name='download_pdf'),
    path('application/<int:application_id>/download/word/', views.download_word, name='download_word'),
    path('application/<int:application_id>/download/excel/', views.download_excel, name='download_excel'),
    path('form_complete/', form_complete, name='form_complete'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),

    path('paynow_payment/<int:application_id>/', views.Paynow_Payment, name='paynow_payment'),
 

   
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('general_payment/', general_payment, name='general_payment'),
    path('payment_timeout/', payment_timeout, name='payment_timeout'),


]