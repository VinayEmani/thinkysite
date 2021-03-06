from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.template import loader
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from .models import Thread, Comment, ThinkyUser, Board, SubForum
from datetime import timezone, datetime
import pytz

# Create your views here.
def index(request):
    return HttpResponse('Welcome to test app django project.')

# user, is_mod, timezone object.
def get_base_context(request, **kwargs):
    user = request.user
    is_mod = False
    if not user.is_authenticated:
        timezone = timezone.utc
    else:
        profile = ThinkyUser.objects.get(user_id=user.id)
        is_mod = profile.is_mod
        try:
            timezone = pytz.timezone(profile.timezone)
        except:
            timezone = timezone.utc
    return dict(user=user, timezone=timezone, is_mod=is_mod)

@require_GET
def homepage(request):
    template = loader.get_template('testapp/homepage.html')
    boards = Board.objects.all()
    forums = SubForum.objects.all()
    boards = [(b.id, (b, [])) for b in boards]
    for f in forums:
        i = 0
        while boards[i][0] != f.board_id:
            i += 1
        boards[i][1][1].append(f)

    def tripartite(lst):
        l = len(lst)
        a, b, c = l // 3, l // 3, l // 3
        if l % 3 >= 1:
            a += 1
        if l % 3 >= 2:
            b += 1
        return (lst[:a], lst[a:a + b], lst[a + b:])

    boards = [(b[0], b[1][0], tripartite(b[1][1])) for b in boards]

    is_mod = False
    if request.user.is_authenticated:
        profile = ThinkyUser.objects.get(user_id=request.user.id)
        is_mod = profile.is_mod

    context = get_base_context(request, is_mod=is_mod)
    context['boards'] = boards
    return HttpResponse(template.render(context, request))

@login_required(login_url='/testapp/loginpage/')
@require_GET
def profilepage(request):
    pid = request.GET.get('pid', None)
    if not pid:
        pid = request.user.id

    if pid == request.user.id:
        profile = request.user
    else:
        try:
            profile = User.objects.get(id=pid)
        except User.DoesNotExist as exe:
            template = loader.get_template('testapp/profilenotfound.html')
            return HttpResponse(template.render(get_base_context(request), request))

    thinky_profile = ThinkyUser.objects.get(user_id=pid)
    pic = thinky_profile.profile_pic or "pics/default-avatar.png"
    template = loader.get_template('testapp/profilepage.html')
    profile_full_name = profile.first_name + ' ' + profile.last_name
    context = get_base_context(request)
    context.update(pic=pic, profile_full_name=profile_full_name,
                   profile=profile)
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

@login_required(login_url='/testapp/loginpage/')
@require_POST
def user_data_update(request):
    pass1, pass2 = request.POST['password'], request.POST['password2']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    if pass1 != pass2:
        return HttpResponseBadRequest('Password confirmation failed')
    elif pass1 and not is_strong_password(pass1):
        return HttpResponseBadRequest('Password confirmation failed')
    else:
        user = request.user
        if pass1:
            user.set_password(pass1)
        if user.first_name != first_name:
            user.first_name = first_name
        if user.last_name != last_name:
            user.last_name = last_name 
        user.save()
        return HttpResponseRedirect('/testapp/profile/')

def is_a_mod(user):
    if not user.is_authenticated:
        return False
    profile = ThinkyUser.objects.get(user_id=user.id)
    return profile.is_mod

@user_passes_test(is_a_mod, redirect_field_name=None)
@require_GET
def modpage(request):
    template = loader.get_template('testapp/modpage.html')
    context = get_base_context(request, is_mod=True)
    all_mods = ThinkyUser.objects.filter(is_mod=True)
    mods_with_names = [(User.objects.get(id=mod.user_id).username, mod) for mod in all_mods]
    boards = Board.objects.all()
    context.update(mods_with_names=mods_with_names, all_mods=all_mods, boards=boards)
    return HttpResponse(template.render(context, request))

@user_passes_test(is_a_mod, redirect_field_name=None)
@require_POST
def addnewmod(request):
    newmodname = request.POST.get('newmod')
    if not newmodname:
        return HttpResponseBadRequest('Bad request, empty username.')
    else:
        users = User.objects.filter(username=newmodname)
        if not users:
            return HttpResponseBadRequest('Bad request, no such user.')
        profile = ThinkyUser.objects.get(user_id=users[0].id)
        if profile.is_mod:
            return HttpResponse('User already a mod.')
        profile.is_mod = True
        profile.save()
        return HttpResponse('Operation success.')

@user_passes_test(is_a_mod, redirect_field_name=None)
@require_POST
def deloldmod(request):
    oldmodname = request.POST.get('oldmod')
    if oldmodname == request.user.username:
        return HttpResponseBadRequest("Bad request, can't unmod yourself.")
    if not oldmodname:
        return HttpResponseBadRequest('Bad request, empty username.')
    else:
        users = User.objects.filter(username=oldmodname)
        if not users:
            return HttpResponseBadRequest('Bad request, no such user.')
        profile = ThinkyUser.objects.get(user_id=users[0].id)
        if not profile.is_mod:
            return HttpResponse('User not a mod.')
        profile.is_mod = False
        profile.save()
        return HttpResponse('Operation success.')

@user_passes_test(is_a_mod, redirect_field_name=None)
@require_GET
def curmodlist(request):
    mods = ThinkyUser.objects.filter(is_mod=True)
    ret = dict()
    for mod in mods:
        usr = User.objects.get(id=mod.user_id)
        ret[usr.username] = mod.user_id
    return JsonResponse(ret)

@require_GET
def board(request):
    boardid = request.GET.get('boardid', None)
    if boardid is None:
        return HttpResponseRedirect('/testapp/home/')
    try:
        board = Board.objects.get(id=boardid)
        forums = SubForum.objects.filter(board_id=boardid)
        context = get_base_context(request)
        context.update(
            name=board.board_name,
            desc=board.board_desc,
            id=boardid,
            forums=forums,
        )
        template = loader.get_template('testapp/boardpage.html')
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template("testapp/boardnotfound.html")
        return HttpResponse(template.render(
            get_base_context(request), request))

@require_GET
def getboards(request):
    boards = Board.objects.all()
    return JsonResponse(
            {b.id: {"name": b.board_name,
                    "desc": b.board_desc} for b in boards})

@user_passes_test(is_a_mod, redirect_field_name=None)
@require_POST
def modboard(request):
    SUCCESS = 0
    FAILURE = 1

    action = request.POST.get('action', None)
    if action not in ('create', 'remove'):
        return JsonResponse(dict(retCode=FAILURE,
                                 explanation="Invalid action"))
    board_name = request.POST.get('boardname', None)
    if not board_name:
        return JsonResponse(dict(retCode=FAILURE,
                                 explanation="Invalid Board name"))
    if action == "create":
        board_desc = request.POST.get('boarddesc', None)
        if not board_desc:
            return JsonResponse(dict(retCode=FAILURE,
                                     explanation="Invalid Board description."))
        if Board.objects.filter(board_name=board_name):
            return JsonResponse(dict(retCode=FAILURE,
                                     explanation="Board name already exists."))
        board = Board(board_name=board_name, board_desc=board_desc)
        board.save()
        return JsonResponse(dict(retCode=SUCCESS,
                                 explanation="Board successfully added."))
    else:
        # board removal not supported yet.
        return HttpResponseBadRequest('Operation not supported.')

@user_passes_test(is_a_mod, redirect_field_name=None)
@require_POST
def modforum(request):
    action = request.POST.get('action', None)

    SUCCESS = 0
    FAILURE = 1

    if action not in ("create", "delete"):
        return JsonResponse(dict(retCode=FAILURE,
                            explanation="Invalid action"))
    if action == "delete":
        return JsonResponse(dict(retCode=FAILURE,
                            explanation="Operation not supported yet"))
    else:
        fname = request.POST.get('name', None)
        fdesc = request.POST.get('desc', None)
        boardid = request.POST.get('boardid', None)
        if not fname or not fdesc:
            return JsonResponse(dict(retCode=FAILURE,
                explanation="Invalid forum name or description"))

        forums = SubForum.objects.filter(board_id=boardid, forum_name=fname)
        if forums:
            return JsonResponse(dict(retCode=FAILURE,
                explanation="A forum already exists with this name in this board"))
        subforum = SubForum(board_id=boardid, forum_name=fname,
                            forum_desc=fdesc)
        subforum.save()
        return JsonResponse(dict(retCode=SUCCESS,
                explanation="Successfully added a new forum"))

@require_GET
def newthread(request):
    context = get_base_context(request)
    forumid = request.GET.get('forumid', None)
    context.update(forumid=forumid)
    template = loader.get_template('testapp/newthread.html')
    return HttpResponse(template.render(context, request))

@login_required(redirect_field_name=None)
@require_POST
def createthread(request):
    # forumid, title, posted_by_id, post_date, thread_type, last_post_time
    forumid = request.POST.get('forumid', None)
    title = request.POST.get('title', None)
    if not title:
        return HttpResponseBadRequest('Title can\'t be empty.')
    posted_by_id = request.user.id
    post_date = datetime.now(tz=timezone.utc)
    try:
        thread = Thread.objects.create(sub_forum_id=forumid,
                    title=title, posted_by_id=posted_by_id,
                    post_date=post_date, last_post_time=post_date,
                    thread_type=0)
        return HttpResponseRedirect('/testapp/forum/?forumid=%s' % forumid)
    except:
        return HttpResponseBadRequest('Failed creating a new thread')

@require_GET
def threadpage(request):
    threadid = request.GET.get('threadid', None)
    if not threadid:
        return HttpResponseBadRequest('Thread not found')

    start = int(request.GET.get('start', '1')) - 1
    count = int(request.GET.get('count', '10'))
    try:
        thread = Thread.objects.get(id=threadid)
        comments = Comment.objects.filter(thread_id=threadid).order_by('post_date')[start:start+count]
        template = loader.get_template('testapp/threadpage.html')
        context = get_base_context(request)
        context.update(thread=thread, start=start, comments=comments)
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponseBadRequest('Invalid request parameters.')


@login_required(redirect_field_name=None)
@require_POST
def newcomment(request):
    threadid = request.GET.get('threadid', None)
    if not threadid:
        return HttpResponseBadRequest('Invalid thread')
    text = request.POST.get('commenttext')
    post_date = datetime.now(tz=timezone.utc)
    start = 0
    try:
        comment = Comment.objects.create(thread_id=threadid,
                posted_by_id=request.user.id, text=text,
                post_date=post_date)
        comment.thread.last_post_time = post_date
        comment.thread.num_comments += 1
        start = max(comment.thread.num_comments - 9, 1)
        comment.thread.save()
    except:
        return HttpResponseBadRequest('Unknown error - invalid thread id likely cause.')
    return HttpResponseRedirect('/testapp/thread/?threadid=%s&start=%s' % (threadid, str(start)))

@require_GET
def forumpage(request):
    forumid = request.GET.get('forumid', None)
    if not forumid:
        return HttpResponse('Invalid forum page')
    try:
        forum = SubForum.objects.get(id=forumid)
        start = request.GET.get('start', 1)
        context = get_base_context(request)
        threads = Thread.objects.filter(sub_forum_id=forumid)
        context.update(forum=forum, threads=threads)
        template = loader.get_template('testapp/forumpage.html')
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('Forum not found')

def is_strong_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password)

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

@require_POST
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('testapp-homepage'))
