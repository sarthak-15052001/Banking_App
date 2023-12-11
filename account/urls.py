from django.urls import path
from .views import *
from account import views

app_name = "account"

urlpatterns = [
    # path("", views.Account, name="account"),
    path('', AccountView.as_view(), name='account'),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('kyc-registration/', KYCCreateView.as_view(), name='kyc_registration'),
]
