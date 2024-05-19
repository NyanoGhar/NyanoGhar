from django.urls import re_path
from . import views

urlpatterns=[
    
    re_path('signup/', views.signup_api, name='signup_api'),
    re_path('login/', views.login_api, name='login_api'),
    re_path('logout/', views.logout_api, name='logout_api'),
]