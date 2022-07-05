from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import *

import json

from .models import Profile


@csrf_exempt
def register_user(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create(
            username=data['surname'],
            email=data['email'],
            password=data['password']
        )
        Profile.objects.create(
            user=user,
            sex=data['sex'] == 'male',
            birth=data['birth']
        )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def login_user(request: HttpRequest):
    if request.method == 'POST':
        for i in request.POST.items():
            print(i)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()


