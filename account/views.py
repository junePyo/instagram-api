import json
import jwt
import bcrypt

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.db.models import Q

from account.models import Account, Follow
from feed.models import *
from settings import SECRET_KEY, HASH


@login_decorator
class ProfileView(View):
    # get method: returns user profile
    def get(self, request):
        jwt.decode()
        profile = {
            'username':}
        # commentsList = serializers.serialize(
        #    "json", account.comment_set.values('text'))
        # return all comments written by the user
        return JsonResponse({f'all comments written by {account}': commentsList}, status=200)


class LoginView(View):
    # def get(self, request):
    #    fields = ['username, email, or phone', 'password']
    #    return JsonResponse(fields, safe=False, status=200)

    # post method: user log-in with any one of username, email, or phone
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
                if bcrypt.checkpw(data['password'].encode('utf-8'), getattr(user, 'password').encode('utf-8')):
                    # if password is correct
                    token = jwt.encode({'user_id': user.id},
                                       SECRET_KEY, algorithm=HASH)
                    return JsonResponse({'message': 'Login Successful!', 'token': token}, status=200)
            return JsonResponse({'message': 'Incorrect id or password'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)


class RegisterView(View):
    # get method:
    # def get(self, request):
    #    fields = ["username", "phone", "email", "password"]
    #    return JsonResponse(fields, safe=False, status=200)

    # post method: user sign-up
    def post(self, request):
        data = json.loads(request.body)
        try:
            e_password = bcrypt.hashpw(
                data['password'].encode('utf-8'), bcrypt.gensalt())
            Account.objects.create(
                username=data['username'],
                phone=data['phone'],
                email=data['email'],
                password=e_password.decode('utf-8'),
            )
            # if registered successfully
            return JsonResponse({'message': 'Registration Successful!'}, status=200)
        except IntegrityError:
            return JsonResponse({'message': 'EXISTING_VALUE'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)
