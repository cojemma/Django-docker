from django.shortcuts import render, redirect
from .models import User, Post
from .utils import Jwt
from django.contrib import messages

# Create your views here.


def home(request):
    user = check_login(request)
    if request.method == 'POST':
        if not user:
            messages.warning(request, '請先登入')
            return redirect('/')
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.delete()
        return redirect('/')
    elif request.GET.get('search_title'):
        search_title = request.GET.get('search_title')
        posts = Post.objects.filter(title__contains=search_title)
    else:
        posts = Post.objects.all()
    return render(request, 'home.html', locals())


def addPost(request):
    user = check_login(request)
    if not user:
        messages.warning(request, '請先登入')
        return redirect('/')
    if request.method == 'POST':
        post_title = request.POST.get('title')
        post_text = request.POST.get('text')
        if post_title:
            post = Post.objects.create(title=post_title, text=post_text)
            return redirect('/')
    return render(request, 'addpost.html')


def editPost(request):
    user = check_login(request)
    if not user:
        messages.warning(request, '請先登入')
        return redirect('/')
    post = Post.objects.get(id=request.GET.get('id'))
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.text = request.POST.get('text')
        post.save()
        return redirect('/')
    return render(request, 'editpost.html', locals())


def login(request):
    if request.method == 'POST':
        username_login = request.POST.get('username')
        password_login = request.POST.get('password')
        user = User.objects.filter(username=username_login, password=password_login)
        if user:
            user = user[0]
            toke = Jwt().encode({'username': user.username})
            request.session['token'] = toke.token
            return redirect('/')
        else:
            messages.warning(request, '尚未註冊該帳戶')
            return redirect('/')
    return render(request, 'login.html')


def check_login(request):
    toke = request.session.get('token', None)
    data = Jwt(toke).decode()
    if data:
        user = data['username']
        return user
    else:
        return False


def logout(request):
    request.session.flush()
    return redirect('/')


def register(request):
    if request.method == 'POST':
        username_regist = request.POST.get('username')
        password_regist = request.POST.get('password')
        if len(password_regist) < 6:
            messages.warning(request, '密碼過短')
            return render(request, 'register.html')
        user = User.objects.create(username=username_regist, password=password_regist)
        messages.info(request, '註冊成功')
        return redirect('/')
    return render(request, 'register.html')

def post(request):
    user = check_login(request)
    if request.GET.get('id'):
        post = Post.objects.get(id=request.GET.get('id'))
        return render(request, 'post.html', locals())
    else:
        return redirect('/')