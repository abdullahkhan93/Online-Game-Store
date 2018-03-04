from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.forms import EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ..models import UserAttributes
import random, string
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.
class SignupForm(UserCreationForm):
    email = EmailField(label=("Email address"), required=True,
        help_text=("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

def is_user_logged_in(request):
    if request.user.is_authenticated:
        return HttpResponse('<h1>Sup man</h1>')
    else:
        return HttpResponse('<h1>log in you scrublet</h1>')

def register_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save(commit=True)
            messages.add_message(request, messages.SUCCESS, 'Please check your e-mail to verify your account')
            return redirect("shop")
    else:
        form = SignupForm()

    return render(request, 'register3.html', {'form': form})


def verify(request, token):
    attributes = UserAttributes.objects.filter(verificationToken=token)
    if len(attributes) > 0:
        user = attributes[0].userID
        user.is_active = True
        user.save()
        return HttpResponse('User {} activated'.format(user.username))
    else:
        return HttpResponse('Invalid verification link')

def changeUser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    
    return redirect('login')