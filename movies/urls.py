from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('payment/', views.add_payment, name='payment'),
    path('add/', views.add, name='add'),
    path('reservation/', views.reservation, name='reservation'),
    path('event/', views.event_form, name='event')
]
