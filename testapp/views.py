from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.template import loader
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from .models import ThinkyUser, Board

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
    pid = request.GET.get('pid', None)
    if not pid:
        pid = request.user.id

    if pid == request.user.id:
        profile = request.user.thinkyuser
    else:
        try:
            profile = ThinkyUser.objects.get(user_id=pid)
        except ThinkyUser.DoesNotExist as exe:
            template = loader.get_template('testapp/profilenotfound.html')
            return HttpResponse(template.render(dict(), request))

    has_pic = profile.profile_pic != ''
    template = loader.get_template('testapp/profilepage.html')
    profile_full_name = profile.user.first_name + ' ' + profile.user.last_name
    context = {
        'user': request.user,
        'has_pic': has_pic,
        'profile_full_name': profile_full_name,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))

class ProfileUpdateForm(forms.Form):
    image = forms.ImageField()

@require_POST
def profile_update(request):
    form = ProfileUpdateForm(request.POST, request.FILES)
    if form.is_valid():
        profile = ThinkyUser.objects.get(user_id=request.user.id)
        profile.profile_pic = form.cleaned_data['image']
        profile.save()
    else:
        messages.add_message(request, messages.INFO,
                "Invalid image file uploaded.")

    return HttpResponseRedirect(reverse('testapp-profilepage'))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name']

@require_POST
def user_data_update(request):
    instance = User.objects.get(id=request.user.id)
    form = UserUpdateForm(request.POST, instance=instance)
    if form.is_valid():
        pass1, pass2 = form.cleaned_data['password'], form.data['password2']
        if pass1 != pass2:
            messages.add_message(request, messages.INFO,
                "Passwords don't match.")
            return HttpResponseRedirect(reverse('testapp-profilepage'))
        elif not is_strong_password(pass1):
            messages.add_message(request, messages.INFO,
                "Password not strong enough.")
            return HttpResponseRedirect(reverse('testapp-profilepage'))

        instance.set_password(form.cleaned_data['password'])
        instance.first_name = form.cleaned_data['first_name']
        instance.last_name = form.cleaned_data['last_name']
        instance.save()
    else:
        for err in form.errors:
            messages.add_message(request, messages.INFO, err)

    return HttpResponseRedirect(reverse('testapp-profilepage'))

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
