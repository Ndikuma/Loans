from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoanViewSet, WalletViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r"loans", LoanViewSet, basename="loan")
router.register(r"wallets", WalletViewSet, basename="wallet")

# Include the router URLs
urlpatterns = [
    path("", include(router.urls)),
    # path('search/', LoanSearchView.as_view(), name='loan-search'),
]
