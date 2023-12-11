from django.shortcuts import render, redirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView, DeleteView, ListView, View
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from account.models import Account
from .models import *
from .forms import *
from django.contrib import messages
from decimal import Decimal
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

#<-------------------------Index View Starts From Here--------------------------------------->
class IndexTemplateView(TemplateView):
    template_name = 'core/index.html'


#<---------------------------Freelancer Payments Template View Starts From Here------------------------->
class FreelancerPayments(TemplateView):
    template_name = 'core/freelancer-payments.html'


#<--------------------------------------------Subscriptions Template View Starts From Here-------------------------->
class SubscriptionsView(TemplateView):
    template_name = 'core/subscriptions.html'

#<-------------------------------------------Security Template View Starts From Here------------------------>
class SecurityTemplateView(TemplateView):
    template_name = 'core/security.html'

#<-------------------------------------------Fees Template View Starts From Here---------------------------->
class FeesTemplateView(TemplateView):
    template_name = 'core/fees.html'

#<------------------------------------------Business Account Template View Starts From Here---------------------------->
class BusinessAccountTemplate(TemplateView):
    template_name = 'core/business-account.html'

#<------------------------------------------Corporate Card Starts From Here-------------------------------------------->
class CorporateCardTemplate(TemplateView):
    template_name = 'core/corporate-card.html'

#<--------------------------------------------Expense Management Starts From Here--------------------------------------->
class ExpenseManagementTemplate(TemplateView):
    template_name = 'core/expense-management.html'

#<-----------------------------------------------Budget Template Starts From Here--------------------------------------->
class BudgetTemplate(TemplateView):
    template_name = 'core/budget.html'

#<-----------------------------------------------Integrations Template Starts from Here---------------------------------->
class IntegrationsTemplate(TemplateView):
    template_name = 'core/integration.html'

#<-----------------------------------------------Company(Paylio) Template Starts From Here------------------------------->
class CompanyTemplate(TemplateView):
    template_name = 'core/company.html'         

#<----------------------------------------------Carrer Template View Starts From Here------------------------------------>
class CareerTemplate(TemplateView):
    template_name = 'core/career.html'

#<----------------------------------------------Blog Template View Starts From Here--------------------------------------->
class BlogTemplate(TemplateView):
    template_name = 'core/blog.html'            


############################################## TRANSAFER ######################################

#<------------------------------Search Account View Starts from Here---------------------->
class SearchUsersByAccountNumberView(LoginRequiredMixin, ListView):
    template_name = 'transfer/search-user-by-account-number.html'
    model = Account
    context_object_name = 'account'

    def post(self, request, *args, **kwargs):
        queryset = self.model.objects.all()
        query = self.request.POST.get("account_number")

        if query:
            queryset = queryset.filter(
                Q(account_number=query) |
                Q(account_id=query)
            ).distinct()

        context = {'account': queryset, 'query': query}
        return render(request, self.template_name, context)


#<------------------------------------------Amount Transfer View Starts From Here--------------------------->
class AmountTransferView(TemplateView):
    template_name = 'transfer/amount-transfer.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_number = kwargs.get('account_number')
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            context['redirect_to_search'] = True
            return context
        context['account'] = account
        return context


    def get(self, request, *args, **kwargs):
        # Get the context data
        context = self.get_context_data(**kwargs)
        
        # Check if the 'redirect_to_search' key is present in the context
        if context.get('redirect_to_search'):
            messages.warning(self.request, "Account does not exist.")
            return redirect("core:search-account")

        # Render the template with the valid context
        return self.render_to_response(context)


#<-------------------------------------Amount Transfer Process View Starts From Here--------------------------------->
class AmountTransferProcessView(View):

    def get(self, request, account_number, *args, **kwargs):
        account = Account.objects.get(account_number=account_number)
        sender = request.user
        reciever = account.user
        sender_account = request.user.account
        reciever_account = account

        context = {
            'account': account,
            'sender': sender,
            'reciever': reciever,
            'sender_account': sender_account,
            'reciever_account': reciever_account,
        }

        return render(request, self.template_name, context)

    def post(self, request, account_number, *args, **kwargs):
        account = Account.objects.get(account_number=account_number)
        sender = request.user
        reciever = account.user
        sender_account = request.user.account
        reciever_account = account

        amount = request.POST.get("amount-send")
        description = request.POST.get("description")


        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                reciever=reciever,
                sender=sender,
                sender_account=sender_account,
                 reciever_account= reciever_account,
                status="processing",
                transaction_type="transfer"
            )
            new_transaction.save()

            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "Insufficient Fund.")
            return redirect("core:amount-transfer", account.account_number)



#<---------------------------------------Transfer Confirmation----------------------------------------->
class TransferConfirmation(TemplateView):
    template_name = "transfer/transfer-confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_number = kwargs.get('account_number')
        transaction_id = kwargs.get('transaction_id')
        try: 
            account = get_object_or_404(Account, account_number=account_number)
            transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        except:
            messages.warning(self.request, "Transaction does not exist.")
            return redirect("account:account")
        messages.success(self.request, "Transaction details loaded successfully.")
        context["account"] = account
        context["transaction"] = transaction
        return context

#<----------------------------------------------Transfer Process view Starts From Here-------------------------->
class TransferProcessView(View):

    def get(self, request, account_number, transaction_id, *args, **kwargs):
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

        sender = request.user
        reciever = account.user

        sender_account = request.user.account
        reciever_account = account

        context = {
            'account': account,
            'transaction': transaction,
            'sender': sender,
            'reciever': reciever,
            'sender_account': sender_account,
            'reciever_account': reciever_account,
            'completed': False,
        } 
        return render(request, self.template_name, context)

    
    def post(self, request, account_number, transaction_id, *args, **kwargs):
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

        sender = request.user
        reciever = account.user

        sender_account = request.user.account
        reciever_account = account

        completed = False

        pin_number = request.POST.get("pin-number")
        # print("---------------------->>>>>>>>>>>>>>", pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status = "Completed"
            transaction.save()

            sender_account.account_balance -= transaction.amount
            sender_account.save()

            account.account_balance += transaction.amount
            account.save()

            # Notification.objects.create(
            #     amount=transaction.amount,
            #     user=account.user,
            #     notification_type="Credit Alert"
            # )

            # Notification.objects.create(
            #     user=sender,
            #     notification_type="Debit Alert",
            #     amount=transaction.amount
            # )

            completed = True
            messages.success(request, "Transfer Successful.")
            return redirect("core:transfer-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin.")
            return redirect('core:transfer-confirmation', account.account_number, transaction.transaction_id)

        context = {
            'account': account,
            'transaction': transaction,
            'sender': sender,
            'reciever': reciever,
            'sender_account': sender_account,
            'reciever_account': reciever_account,
            'completed': completed,
        }

        return render(request, self.template_name, context)

#<-------------------------------------------Transfer Complete Views Starts From Here------------------------>
class TransferCompletedView(TemplateView):
    template_name = "transfer/transfer-completed.html"

    def get_context_data(self, **kwargs):
        account_number = kwargs.get('account_number')
        transaction_id = kwargs.get('transaction_id')
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

        # Check if necessary data is present, otherwise redirect
        if not account or not transaction:
            messages.warning(self.request, "Transfer does not exist.")
            return HttpResponseRedirect(reverse("account:account"))

        context = {
            "account": account,
            "transaction": transaction
        }
        return context


############################################ TRANSACTIONS ###########################################

#<-----------------------------------Transaction List View Starts From Here--------------------------->
class TransactionListView(LoginRequiredMixin, ListView):
    template_name = "transaction/transaction-list.html"

    def get_queryset(self):
        # Return an empty queryset since the transactions are fetched in get_context_data
        return Transaction.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        sender_transaction = Transaction.objects.filter(sender=user, transaction_type="transfer").order_by("-id")
        reciever_transaction = Transaction.objects.filter(reciever=user, transaction_type="transfer").order_by("-id")
        request_sender_transaction = Transaction.objects.filter(sender=user, transaction_type="Request")
        request_reciever_transaction = Transaction.objects.filter(reciever=user, transaction_type="Request")

        context['sender_transaction'] = sender_transaction
        context['reciever_transaction'] = reciever_transaction
        context['request_sender_transaction'] = request_sender_transaction
        context['request_reciever_transaction'] = request_reciever_transaction
        return context

#<---------------------------------------------Transaction Detail View Starts From Here--------------------------->
class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "transaction/transaction-detail.html"
    context_object_name = "transaction"
    slug_field = "transaction_id"
    slug_url_kwarg = "transaction_id"



############################################ PAYMENT OR AMOUNT   REQUEST ###########################################

#<---------------------------------Search Users Request View Starts From Here-------------------------->
class SearchUsersRequest(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'payment_request/search-users.html'
    context_object_name = 'accounts'



    def post(self, request, *args, **kwargs):
        queryset = self.model.objects.all()
        query = self.request.POST.get("account_number")

        if query:
            queryset = queryset.filter(
                Q(account_number=query) |
                Q(account_id=query)
            ).distinct()

        context = {'account': queryset, 'query': query}
        return render(request, self.template_name, context)


#<-----------------------------------------Amount Request View Starts From Here------------------------------>
class AmountRequest(TemplateView):
    template_name = 'payment_request/amount-request.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_number = kwargs.get('account_number')
        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            context['redirect_to_search'] = True
            return context
        context['account'] = account
        return context


    def get(self, request, *args, **kwargs):
        # Get the context data
        context = self.get_context_data(**kwargs)
        
        # Check if the 'redirect_to_search' key is present in the context
        if context.get('redirect_to_search'):
            messages.warning(self.request, "Account does not exist.")
            return redirect("core:request-search-account")

        # Render the template with the valid context
        return self.render_to_response(context)


#<-----------------------------Amount Request Process View Starts From Here-------------------------------->
class AmountRequestProcessView(View):

    def get(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
            sender_account = request.user.account
            reciever_account = account
        except Account.DoesNotExist:
            messages.warning(request, "Error occurred. Try again later.")
            return redirect("account:dashboard")
        return render(request, self.template_name, {'account':account})

    
    def post(self, request, account_number):
        try:
            account = Account.objects.get(account_number=account_number)
            sender = request.user
            reciever = account.user
            sender_account = request.user.account
            reciever_account = account
        except Account.DoesNotExist:
            messages.warning(request, "Error occured. Try again later.")
            return redirect("account:dashboard")

        amount = request.POST.get("amount-request")
        description = request.POST.get("description")
        status = "Request_Processing"
        transaction_type = "Request"

        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            sender=sender,
            reciever=reciever,
            sender_account=sender_account,
            reciever_account=reciever_account,
            status=status,
            transaction_type=transaction_type
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)


#<---------------------------------------Amount Request Confirmation Starts From Here------------------------------------>
class AmountRequestConfirmation(TemplateView):
    template_name = 'payment_request/amount-request-confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_number = kwargs.get('account_number')
        transaction_id = kwargs.get('transaction_id')
        try: 
            account = get_object_or_404(Account, account_number=account_number)
            transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        except:
            messages.warning(self.request, "Transaction does not exist.")
            return redirect("account:account")
        messages.success(self.request, "Transaction details loaded successfully.")
        context["account"] = account
        context["transaction"] = transaction
        return context


#<------------------------------Amount Request Final Process View --------------------------------------------->
class AmountRequestFinalProcessView(View):
    

    def get(self, request, account_number, transaction_id):
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

        context = {'account': account, 'transaction': transaction}
        return render(request, self.template_name, context)


    def post(self, request, account_number, transaction_id):
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

        if request.method == "POST":
            pin_number = request.POST.get("pin-number")
            if pin_number == request.user.account.pin_number:
                transaction.status = "Request_Sent"
                transaction.save()

                # Notification.objects.create(
                #     user=account.user,
                #     notification_type="Received Payment Request",
                #     amount=transaction.amount,
                # )

                # Notification.objects.create(
                #     user=request.user,
                #     amount=transaction.amount,
                #     notification_type="Sent Payment Request"
                # )

                messages.success(request, "Your payment request has been sent successfully.")
                return redirect("core:amount-request-completed", account.account_number, transaction.transaction_id)
            else:
                messages.warning(request, "Incorrect PIN number. Please try again.")
        else:
            messages.warning(request, "An Error Occurred. Please try again later.")

        return redirect("account:dashboard")



#<------------------------------------------Request Completed View Starts From Here----------------------------->
class RequestCompleted(TemplateView):
    template_name = 'payment_request/amount-request-completed.html'


    def get_context_data(self, **kwargs):
        account_number = kwargs.get('account_number')
        transaction_id = kwargs.get('transaction_id')
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

        # Check if necessary data is present, otherwise redirect
        if not account or not transaction:
            messages.warning(self.request, "Transfer does not exist.")
            return HttpResponseRedirect(reverse("account:account"))

        context = {
            "account": account,
            "transaction": transaction
        }
        return context


#################################################### SETTLED #########################################

#<-------------------------------------------Settlement Confirmation View Starts From Here--------------------------------------->
class SettlementConfirmation(TemplateView):
    template_name = 'payment_request/settlement-confirmation.html'

    def get_context_data(self, **kwargs):
        account_number = kwargs.get('account_number')
        transaction_id = kwargs.get('transaction_id')

        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id) 

        context = {
            "account": account,
            "transaction": transaction,
        }
        return context


#<------------------------------------------Settlement Processing View Starts From Here----------------------------->   
class SettlementProcessing(View):


    def get(self, request, account_number, transaction_id):
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        sender_account = request.user.account
        context = {
            'account': account,
            'transaction': transaction,
            'sender_account': sender_account,
        }
        return render(request, self.template_name, context)


    def post(self, request, account_number, transaction_id):
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        sender_account = request.user.account

        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(request, "Insufficient Funds")
            else:
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()

                transaction.status = "Request_Settled"
                transaction.save()

                messages.success(request, "Your Payment was sent successfully")
                return redirect("core:settlement-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect("core:settlement-confirmation", account.account_number, transaction.transaction_id)


#<----------------------------------------------Settlement Completed----------------------------------------------->
class SettlementCompleted(TemplateView):
    template_name = "payment_request/settlement-completed.html"

    def get_context_data(self, **kwargs):
        account_number = kwargs.get("account_number")
        transaction_id = kwargs.get("transaction_id")

        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

        if not account or not transaction:
            messages.warning(self.request, "Transfer does not exist.")
            return HttpResponseRedirect(reverse("account:account"))

        context = {
            "account": account,
            "transaction": transaction
        }
        return context

#<-------------------------------------Delete Payment Request Starts From Here----------------------------->
# def DeletePaymentRequest(request, account_number ,transaction_id):
#     account = Account.objects.get(account_number=account_number)
#     transaction = Transaction.objects.get(transaction_id=transaction_id)

#     if request.user == transaction.user:
#         transaction.delete()
#         messages.success(request, "Payment Request Deleted Sucessfully")
#         return redirect("core:transaction-list") 


class DeletePaymentRequest(View):
    success_url = reverse_lazy('core:transaction-list')

    def get(self, request, *args, **kwargs):
        account_number = self.kwargs.get('account_number')
        transaction_id = self.kwargs.get('transaction_id')
        
        account = get_object_or_404(Account, account_number=account_number)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

        if request.user == transaction.user:
            transaction.delete()
            messages.success(request, "Payment Request Deleted Successfully")
            return redirect(self.success_url)

        # Handle the case where the user is not authorized to delete the transaction
        messages.error(request, "You are not authorized to delete this payment request")
        return redirect(self.success_url)

############################################ CREDIT CARD #######################################################

#<------------------------------------------Credit Card Detail View Starts From Here----------------------------------->
class CreditCardDetail(DetailView):
    model = CreditCard
    template_name = 'credit_card/card-detail.html'
    context_object_name = 'credit_card'
    slug_url_kwarg = 'card_id'
    slug_field = 'card_id'

    def get_queryset(self):
        return CreditCard.objects.filter(user=self.request.user)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = Account.objects.get(user=self.request.user)
        return context


#<---------------------------------------------Fund Credit Card View Starts From Here--------------------------------------> 
class FundCreditCardView(View):

    def get (self, request, card_id):
        credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
        account = request.user.account
        context = {
            'credit_card': credit_card,
            'account': account,
        }
        return render(request, self.template_name,  context)

    def post(self, request, card_id):
        credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
        account = request.user.account
        amount = request.POST.get("funding_amount")

        if Decimal(amount) <= account.account_balance:
            account.account_balance = F('account_balance') - Decimal(amount)
            account.save()

            credit_card.amount = F('amount') + Decimal(amount)
            credit_card.save()

            # Notification.objects.create(
            #     amount=amount,
            #     user=request.user,
            #     notification_type="Funded Credit Card"
            # )

            messages.success(request, "Funding Successful")
            return redirect("core:card-detail", card_id)
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:card-detail", card_id)


#<--------------------------------------------Withdraw Fund Starts From Here--------------------------------->
class WithdrawFundView(View):
    
    def get(self, request, card_id, *args, **kwargs):
        account = get_object_or_404(Account, user=self.request.user)
        credit_card = get_object_or_404(CreditCard, card_id=card_id, user=self.request.user)
        context = {
            'account':account,
            'credit_card':credit_card,
        }
        return render(request, self.template_name, context)


    def post(self, requset, card_id, *args, **kwargs):
        account = get_object_or_404(Account, user=self.request.user)
        credit_card = get_object_or_404(CreditCard, card_id=card_id, user=self.request.user)

        amount = self.request.POST.get("amount")

        if credit_card.amount >= Decimal(amount) and credit_card.amount != 0.00:
            account.account_balance += Decimal(amount)
            account.save()

            credit_card.amount -= Decimal(amount)
            credit_card.save()

            # Notification.objects.create(
            #     user=request.user,
            #     amount=amount,
            #     notification_type="Withdrew Credit Card Funds"
            # )

            messages.success(self.request, "Withdrawal Successful")
            return redirect("core:card-detail", credit_card.card_id)
        else:
            messages.warning(self.request, "Insufficient Funds")
            return redirect("core:card-detail", credit_card.card_id)

#<------------------------------------------Delete Card View Starts From Here-------------------------------->
class DeleteCardView(View):

    def get(self, request, card_id, *args, **kwargs):
        credit_card = get_object_or_404(CreditCard, card_id=card_id, user=request.user)
        account = request.user.account

        if credit_card.amount > 0:
            account.account_balance += credit_card.amount
            account.save()

            # Notification.objects.create(
            #     user=request.user,
            #     notification_type="Deleted Credit Card"
            # )
        
        credit_card.delete()
        messages.success(request, "Card Deleted Successfully")
        return redirect("account:dashboard")