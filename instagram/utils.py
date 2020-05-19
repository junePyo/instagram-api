import jwt
import json

from django.http import JsonResponse
from settings import SECRET_KEY, HASH
from account.models import Account


def login_decorator(func):
    def wrapper(self, request):
        try:
            user_token = request.headers.get('Authorization')
            user_info = jwt.decode(user_token, SECRET_KEY, HASH)
            user = Account.objects.get(user_info['user_id'])
            request.user = user  # request 에 존재하지 않던 user 정보를 추가
            func(self, request)
        except Account.DoesNotExist:
            return JsonResponse({'message': 'Account is not valid'}, status=401)
        except KeyError:  # 'user_id' key does not exist or is invalid
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)
            # user id 가 존재하지 않을수도 잇고
            # header 에 토큰 자체가 없을수도 있고
            # user id 는 존재하나, user object 가 저장이안되있을수 있음
    return wrapper
