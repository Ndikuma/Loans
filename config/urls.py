from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def trigger_error(request):
    division_by_zero = 1 / 0
    return HttpResponse(division_by_zero)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
    path("", include("config.apps.Loan.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
]
