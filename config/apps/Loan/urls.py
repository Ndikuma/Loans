from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import LoanSearchAPIView, LoanViewSet, WalletViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r"loans", LoanViewSet, basename="loan")
router.register(r"wallets", WalletViewSet, basename="wallet")


# Include the router URLs
urlpatterns =[
    path("api/loans/search/", LoanSearchAPIView.as_view(), name="loan_search_api"),
    path("", include(router.urls)),
    # path('search/', LoanSearchView.as_view(), name='loan-search'),,
    path("auth/",include("dj_rest_auth.urls")),
    path("register/",  include('dj_rest_auth.registration.urls')),

  
]
