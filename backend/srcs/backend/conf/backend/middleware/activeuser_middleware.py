import datetime
from django.core.cache import cache
from django.conf import settings
from users.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActiveUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    # def __call__(self, request):
    #     self.process_request(request)
    #     response = self.get_response(request)
    #     return response

    # def process_request(self, request):
    #     if request.user.is_authenticated:
    #         now = datetime.datetime.now()
    #         cache.set('seen_%s' % (request.user.username), now,
    #                        settings.USER_ONLINE_TIMEOUT)

    def __call__(self, request):
        if request.user.is_authenticated:
            chat_key = f'user_online_{request.user.id}'
            if not cache.get(chat_key):
                user = request.user
                user.update_last_seen()
                user.update_is_online()
        response = self.get_response(request)
        return response

# # ALternative:
# from django.utils import timezone

# class ActiveUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             cache_key = f'user_online_{request.user.id}'
#             if not cache.get(cache_key):
#                 # Se não estiver no cache, mas autenticado, pode ser uma sessão antiga
#                 request.user.is_online = False
#                 request.user.save()
#         response = self.get_response(request)
#         return response