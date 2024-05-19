from django.urls import re_path
from . import views

urlpatterns=[
    
    re_path('signup/', views.signup, name='signup_api'),
    re_path('login/', views.login, name='login_api'),
    re_path('logout/', views.test_token, name='logout_api'),
]