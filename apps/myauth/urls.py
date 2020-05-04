from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from apps.myauth.views import *

urlpatterns = [
    re_path('^registration/$', RegistrationChoiceView.as_view(), name='registration_choice'),
    path('registration/author', RegistrationAuthorView.as_view(), name='registration_author'),
    path('registration/consumer', RegistrationConsumerView.as_view(), name='registration_consumer'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html'),
         name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'),
         name='password_change_done'),

    path('password_reset/', PasswordResetView.as_view(),
         name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
