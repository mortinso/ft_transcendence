from django.shortcuts import render
from django.http import HttpResponse, Http404


class NotFoundHTML(Http404):
    def __init__(self, detail=None):
        self.detail = detail or "Not found."

    def __call__(self, request):
        response = render(request, '404.html')
        response.status_code = 404
        return response
