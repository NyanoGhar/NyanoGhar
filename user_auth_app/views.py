from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
def signup(request):
    return Response({})


@api_view(['POST'])
def login(request):
    return Response({})


@api_view(['POST'])
def testapi(request):
    return Response({})