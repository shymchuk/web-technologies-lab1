from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user),
    path('register', views.register_user),
    path('person', views.person),
    path('phone', views.phone),
]
