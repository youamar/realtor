from django.urls import path

from . import views

urlpatterns = [
    path('connection', views.register,name='register'),
    path('login', views.loginUser,name='login'),
    path('list_users', views.odooUsers,name='odoo_connection'),
]