from django.http import HttpResponseBadRequest, Http404
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FrontendOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of allowed referers
        allowed_referers = settings.ALLOWED_REFERERS

        # Check the Referer header
        referer = request.headers.get("Referer")

        if referer is None:
            return HttpResponseBadRequest()

        if not any(referer.startswith(allowed_referer) for allowed_referer in allowed_referers):
            return HttpResponseBadRequest()

        response = self.get_response(request)
        return response
