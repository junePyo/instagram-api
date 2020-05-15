import json
import jwt

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.db.models import Q

from account.models import Account, Follow
from feed.models import *


def profile(request):  # get user profile
    commentsList = []
    account = Account.objects.get(pk=account_pk)
    commentsList.append(list(account.comment_set.values('text')))
    # commentsList = serializers.serialize(
    #    "json", account.comment_set.values('text'))
    # return all comments written by the user
    return JsonResponse({f'all comments written by {account}': commentsList}, status=200)


def mainView(request):  # returns the home page view of Instagram
    return JsonResponse({'message': 'Welcome'}, status=200)


class LoginView(View):
    # display fields that need to be filled to log in
    def get(self, request):
        fields = ['username, email, or phone', 'password']
        return JsonResponse(fields, safe=False, status=200)

    # log in with any one of username, email, or phone number
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(
                Q(username=data['username']) |
                Q(email=data['enmail']) |
                Q(phone=data['phone'])
            ).exists():
                user = Account.objects.get(
                    Q(username=data['username']) |
                    Q(email=data['email']) |
                    Q(phone=data['phone'])
                )
                if getattr(user, 'password') == data['password']:
                    # if logged in successfully
                    return JsonResponse({'message': 'Login Successful!'}, status=200)
            return JsonResponse({'message': 'Incorrect id or password'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)


class RegisterView(View):
    # display fields that need to be filled to sign up
    def get(self, request):
        fields = ["username", "phone", "email", "password"]
        return JsonResponse(fields, safe=False, status=200)

    # signing up
    def post(self, request):
        data = json.loads(request.body)
        try:
            Account.objects.create(
                username=data['username'],
                phone=data['phone'],
                email=data['email'],
                password=data['password'],
            )
            # if registered successfully
            return JsonResponse({'message': 'Registration Successful!'}, status=200)
        except IntegrityError:
            return JsonResponse({'message': 'EXISTING_VALUE'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)
