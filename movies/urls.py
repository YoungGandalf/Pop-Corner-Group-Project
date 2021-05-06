from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('payment/', views.add_payment, name='payment'),
    path('add/', views.add, name='add'),
    path('reservation/', views.reservation, name='reservation'),
    path('event/', views.event_form, name='event'),
    path('edit_reservation/', views.edit_reservation, name='edit_reservation'),
    path('delete_reservation/', views.delete_reservation, name='delete_reservation'),
    path('finish_payment/', views.finish_payment, name='finish_payment'),

    # URLS for resetting password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_recovery/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_recovery/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_recovery/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_recovery/password_reset_complete.html'),
         name='password_reset_complete')
]
