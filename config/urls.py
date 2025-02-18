from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf import settings
from django.conf.urls.static import static

def trigger_error(request):
    division_by_zero = 1 / 0
    return HttpResponse(division_by_zero)


# 122879
urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
    path("", include("config.apps.Loan.urls")),
    path("search/", include("config.apps.search.urls")),
    # Silk monitoring endpoint
    path("silk/", include("silk.urls", namespace="silk")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    # Schema generation endpoint
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Swagger UI
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    #user endpoint
    path("users/", include("config.apps.authantification.urls")),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)