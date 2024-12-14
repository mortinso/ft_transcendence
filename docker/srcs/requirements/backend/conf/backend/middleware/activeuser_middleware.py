import datetime
from django.core.cache import cache
from django.conf import settings
from users.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActiveUserMiddleware():

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
        response = self.get_response(request)
        if request.user.is_authenticated:
            user = request.user
            user.update_last_seen()
            user.update_is_online()
        return response