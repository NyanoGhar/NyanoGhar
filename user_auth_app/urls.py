from django.urls import re_path
from . import views

urlpatterns=[
    
    re_path('signup/', views.SignUp.as_view(), name='signup_api'),
    re_path('login/', views.Login.as_view(), name='login_api'),
    re_path('profile/',views.UserProfileUpdateAPIView.as_view(),name="user-profile-update"),
    re_path('health/',views.Health.as_view(),name="health")

    # re_path('logout/', views.test_token, name='logout_api'),
]
