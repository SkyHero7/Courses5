from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, UserLoginForm

class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm

class CustomLogoutView(LogoutView):
    next_page = 'home'
