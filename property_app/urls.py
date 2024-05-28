from django.urls import path
from . import views

urlpatterns=[
    path('get_properties/', views.PropertyListAPIView.as_view(), name='property-list-create'),
    path('post_properties/', views.PropertyCreateAPIView.as_view(), name='property-list-create'),
    path('images/', views.ImageViewSet.as_view(), name='image-create'),
    path('owner_properties/', views.OwnerPropertyListAPIView.as_view(), name='owner-property-list'),
]