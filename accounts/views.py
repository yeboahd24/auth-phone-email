from django.contrib.auth import views as auth_views
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = "login.html"
    success_message = "You were successfully logged in."
    success_url = 'home'
    



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy(
        "login"
    )  # Replace 'login' with the name of your login view
    template_name = "signup.html"
