from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.template import loader
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Board

# Create your views here.
def index(request):
    return HttpResponse('Welcome to test app django project.')

@require_GET
def homepage(request):
    template = loader.get_template('testapp/homepage.html')
    boards = Board.objects.all()
    context = {
        'boards': boards,
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/testapp/loginpage/')
@require_GET
def profilepage(request):
    template = loader.get_template('testapp/profilepage.html')
    context = {
        'user': request.user,
    }

    return HttpResponse(template.render(context, request))

def is_strong_password(password):
    if len(password) < 8:
        return False
    return any(not c.isdigit() for c in password)

@require_POST
def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    email = request.POST.get('email')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')

    if password != password2:
        messages.add_message(request, messages.INFO, 
                'Passwords didn\'t match. Retry')
        return HttpResponseRedirect(reverse('testapp-signup-page'))

    if not is_strong_password(password):
        messages.add_message(request, messages.INFO,
            'Password is too weak. Atleast 8 characters with atleast one digit.')
        return HttpResponseRedirect(reverse('testapp-signup-page'))

    if not firstname or not lastname:
        messages.add_message(request, messages.INFO,
            'First name and last name cannot be empty. Retry.')
        return HttpResponseRedirect(reverse('testapp-signup-page'))

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.INFO,
            'Invalid email address. Retry.')
        return HttpResponseRedirect(reverse('testapp-signup-page'))
    else:
        pass

    user = User.objects.filter(username=username)
    if user:
        messages.add_message(request, messages.INFO,
            "Username already taken. Retry.")
        return HttpResponseRedirect(reverse('testapp-signup-page'))

    user = User.objects.create_user(username=username, password=password,
                       email=email, first_name=firstname, last_name=lastname)
    login(request, user)
    return HttpResponseRedirect(reverse('testapp-homepage'))

def signuppage(request):
    template = loader.get_template('testapp/signuppage.html')
    context = dict()
    return HttpResponse(template.render(context, request))

@require_http_methods(['POST'])
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponse('You\'re already logged in.')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        return HttpResponse('Failed login attempt.')
    else:
        login(request, user)
        return HttpResponseRedirect(reverse('testapp-homepage'))

@require_GET
def loginpage(request):
    template = loader.get_template('testapp/loginpage.html')
    return HttpResponse(template.render(dict(), request))

@require_GET
def logoutpage(request):
    template = loader.get_template('testapp/logoutpage.html')
    return HttpResponse(template.render(dict(), request))

@require_http_methods(['POST'])
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('testapp-homepage'))
