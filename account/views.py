from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from core.models import *
from .forms import *
from core.forms import CreditCardForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

#<------------------------------------------Account View Starts From Here----------------------------------------->
class AccountView(CreateView):
    template_name = 'account/account.html'
    form_class = KYCForm
    success_url = reverse_lazy("core:index")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need to login to access the dashboard")
            return redirect("userauths:sign-in")

        return super().dispatch(request, *args, **kwargs)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            kyc = KYC.objects.get(user=self.request.user)
            account = Account.objects.get(user=self.request.user)
        except KYC.DoesNotExist:
            messages.warning(self.request, "You need to submit your KYC.")
            return redirect("account:kyc-registration")
        except Account.DoesNotExist:
            messages.warning(self.request, "Account does not exist")
            return redirect("account:account")
        context["kyc"] = kyc
        context["account"] = account
        return context
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, "KYC submitted successfully!")
        return super().form_valid(form)




#<-------------------------------------------------KYCCreate View Starts From Here--------------------------->
@method_decorator(login_required, name='dispatch')
class KYCCreateView(CreateView):
    model = KYC
    form_class = KYCForm
    template_name = "account/kyc-form.html"
    success_url = reverse_lazy("account:account")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            account = get_object_or_404(Account, user=user)
            kyc = KYC.objects.filter(user=user).first()
        else:
            account = None
            kyc = None
        context['account'] = account
        context['kyc'] = kyc
        return context

    def form_valid(self, form):
        user = self.request.user
        account = get_object_or_404(Account, user=user)
        form.instance.user = user
        form.instance.account = account
        response = super().form_valid(form)
        account.account_status = "active"
        account.save()
        messages.success(self.request, "KYC Form submitted successfully, In review now.")
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['instance'] = KYC.objects.filter(user=self.request.user).first()
        return kwargs



#<------------------------------------Dashboard View Starts From Here------------------------------->
class DashboardView(TemplateView):
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:  
            try:
                kyc = KYC.objects.get(user=self.request.user)
            except KYC.DoesNotExist:
                messages.warning(self.request, "You need to submit your kyc")
                return redirect("account:kyc-registration")

            recent_transfer = Transaction.objects.filter(sender=self.request.user, transaction_type="transfer", status="completed").order_by("-id")[:1]
            recent_recieved_transfer = Transaction.objects.filter(reciever=self.request.user, transaction_type="transfer").order_by("-id")[:1]

            sender_transaction = Transaction.objects.filter(sender=self.request.user, transaction_type="transfer").order_by("-id")
            reciever_transaction = Transaction.objects.filter(reciever=self.request.user, transaction_type="transfer").order_by("-id")

            request_sender_transaction = Transaction.objects.filter(sender=self.request.user, transaction_type="Request")
            request_reciever_transaction = Transaction.objects.filter(reciever=self.request.user, transaction_type="Request")

            account = Account.objects.get(user=self.request.user)
            credit_card = CreditCard.objects.filter(user=self.request.user).order_by("-id")

            context.update({
                "kyc": kyc,
                "account": account,
                "form": CreditCardForm(),
                "credit_card": credit_card,
                "sender_transaction": sender_transaction,
                "reciever_transaction": reciever_transaction,
                'request_sender_transaction': request_sender_transaction,
                'request_reciever_transaction': request_reciever_transaction,
                'recent_transfer': recent_transfer,
                'recent_recieved_transfer': recent_recieved_transfer,
            })
        else:
            messages.warning(self.request, "You need to login to access the dashboard")
            return redirect("userauths:sign-in")
        return context


    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()

                # Notification.objects.create(
                #     user=request.user,
                #     notification_type="Added Credit Card"
                # )

                card_id = new_form.card_id
                messages.success(request, "Card Added Successfully.")
                return redirect("account:dashboard")

        return super().get(request, *args, **kwargs)