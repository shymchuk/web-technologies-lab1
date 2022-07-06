from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import *

import json

from .models import Profile, PhoneNumber, Person


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


@csrf_exempt
def person(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        surname = data['surname']
        p = Person.objects.create(surname=surname)
        return JsonResponse({ 'id': p.pk })
    elif request.method == 'GET':
        data = json.loads(request.body)
        if 'id' in data:
            p = Person.objects.get(pk=data['id'])
            return JsonResponse({ 'id': p.pk, 'phones': [x.pk for x in p.phone.all()], 'surname': p.surname })
        else:
            persons = Person.objects.all()
            return JsonResponse({'data': [{ 'id': p.pk, 'phones': [x.pk for x in p.phone.all()], 'surname': p.surname } for p in persons]})
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        if 'id' in data:
            Person.objects.get(pk=data['id']).delete()
        else:
            Person.objects.all().delete()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def phone(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_id, phone_number = data['personId'], data['number']
        p = Person.objects.get(pk=person_id)
        n, _ = p.phone.get_or_create(number=phone_number)
        return JsonResponse({ 'id': n.pk })
    elif request.method == 'GET':
        data = json.loads(request.body)
        id = data['id']
        p = PhoneNumber.objects.get(pk=id)
        return JsonResponse({ 'phone': p.number })
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        person_id, phone_id = data['personId'], data['phoneId']
        p = Person.objects.get(pk=person_id)
        p.phone.remove(PhoneNumber.objects.get(pk=phone_id))
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
