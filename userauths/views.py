from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, AuthenticationForm, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

# Create your views here.

class SignupView(CreateView):
    template_name = 'userauths/sign-up.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy("userauths:sign-in")

    def form_valid(self, form):
        new_user = form.save()
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Hey {username}, your registration was done successfully.")
        new_user = authenticate(
            username = form.cleaned_data['email'],
            password = form.cleaned_data['password1']
        )
        login(self.request, new_user)
        return super().form_valid(form)


class LoginView(LoginView):
    Authentication_Form = UserLoginForm
    template_name = 'userauths/sign-in.html'


    def get_success_url(self):
        return reverse_lazy("account:kyc_registration") 


class LogoutView(LogoutView):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("userauths:sign-in")