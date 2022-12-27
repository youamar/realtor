from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login,name='buyer_login'),
    path('register', views.register,name='buyer_register'),
    path('list', views.apartments,name='buyer_list'),
    path('offer', views.offer,name='offer'),
]