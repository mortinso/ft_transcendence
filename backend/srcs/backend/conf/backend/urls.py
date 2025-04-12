"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("api/users/", include("users.urls")),
    path("api/auth/", include("auth.urls")),
    path("api/oauth/", include("oauth.urls")),
    path("api/users/games/", include("games.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('__debug__/', include(debug_toolbar.urls)),
    ]


# test view for debugging
from django.http import HttpResponse


def debug_test_view(request):
    return HttpResponse("<html><body>Debug Test Page</body></html>", content_type="text/html")


urlpatterns += [
    path('__debug_test__/', debug_test_view, name='debug-test'),
]
