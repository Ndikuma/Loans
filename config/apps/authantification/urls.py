
from django.urls import path
from rest_framework import routers

from .views import UserViewSet,RoleViewSet

router = routers.DefaultRouter()


router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = router.urls