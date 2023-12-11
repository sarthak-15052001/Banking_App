from django.urls import path
from core import views


app_name = "core"

urlpatterns = [ 
    path('', views.IndexTemplateView.as_view(), name="index"),
    path('freelancer-payments/', views.FreelancerPayments.as_view(), name="freelancer-payments"),
    path('subscriptions/', views.SubscriptionsView.as_view(), name="subscriptions"),
    path('security/', views.SecurityTemplateView.as_view(), name="security"),
    path('fees/', views.FeesTemplateView.as_view(), name="fees"),
    path('business-account/', views.BusinessAccountTemplate.as_view(), name="business-account"),
    path('corporate-card/', views.CorporateCardTemplate.as_view(), name="corporate-card"),
    path('expense-management/', views.ExpenseManagementTemplate.as_view(), name="expense-management"),
    path('budget/', views.BudgetTemplate.as_view(), name="budget"),
    path('integration/', views.IntegrationsTemplate.as_view(), name="integration"),
    path('company/', views.CompanyTemplate.as_view(), name="company"),
    path('career/', views.CareerTemplate.as_view(), name="career"),
    path('blog/', views.BlogTemplate.as_view(), name="blog"),

    # Transfers
    path('search-account/', views.SearchUsersByAccountNumberView.as_view(), name="search-account"),
    path('amount-transfer/<str:account_number>/', views.AmountTransferView.as_view(), name="amount-transfer"),
    path('amount-transfer-process/<str:account_number>/', views.AmountTransferProcessView.as_view(), name="amount-transfer-process"),
    path('transfer-confirmation/<str:account_number>/<str:transaction_id>/', views.TransferConfirmation.as_view(), name="transfer-confirmation"),
    path('transfer-process/<str:account_number>/<str:transaction_id>/', views.TransferProcessView.as_view(), name="transfer-process"),
    path('transfer-completed/<str:account_number>/<str:transaction_id>/', views.TransferCompletedView.as_view(), name="transfer-completed"),
  
    # Transactions
    path('transaction-list/', views.TransactionListView.as_view(), name="transaction-list"),
    path('transaction-detail/<str:transaction_id>/', views.TransactionDetailView.as_view(), name='transaction-detail'),

    # Payment Request
    path('request-search-account/', views.SearchUsersRequest.as_view(), name="request-search-account"),
    path('amount-request/<str:account_number>/', views.AmountRequest.as_view(), name="amount-request"),
    path('amount-request-process/<str:account_number>/', views.AmountRequestProcessView.as_view(), name="amount-request-process"),
    path('amount-request-confirmation/<str:account_number>/<str:transaction_id>/', views.AmountRequestConfirmation.as_view(), name="amount-request-confirmation"),
    path('amount-request-final-process/<str:account_number>/<str:transaction_id>/', views.AmountRequestFinalProcessView.as_view(), name="amount-request-final-process"),
    # path("amount-request-final-process/<account_number>/<transaction_id>/", views.AmountRequestFinalProcess, name="amount-request-final-process"),
    path('amount-request-completed/<str:account_number>/<str:transaction_id>/', views.RequestCompleted.as_view(), name="amount-request-completed"),
   
     # Request Settlement
     path('settlement-confirmation/<str:account_number>/<str:transaction_id>/', views.SettlementConfirmation.as_view(), name="settlement-confirmation"),
     path('settlement-processing/<str:account_number>/<str:transaction_id>/', views.SettlementProcessing.as_view(), name="settlement-processing"),
     path('settlement-completed/<str:account_number>/<str:transaction_id>/', views.SettlementCompleted.as_view(), name="settlement-completed"),
     path("delete-request/<str:account_number>/<str:transaction_id>/", views.DeletePaymentRequest.as_view(), name="delete-request"),
    # path('delete-request/account_number>/transaction_id/', views.DeletePaymentRequest, name="delete-request"),

    # Credit Card
    path('card-detail/<str:card_id>/', views.CreditCardDetail.as_view(), name="card-detail"),
    path('fund-credit-card/<str:card_id>/', views.FundCreditCardView.as_view(), name="fund-credit-card"),
    path('withdraw-fund/<str:card_id>/', views.WithdrawFundView.as_view(), name="withdraw-fund"),
    path('delete-card/<str:card_id>/', views.DeleteCardView.as_view(), name="delete-card"),
]
