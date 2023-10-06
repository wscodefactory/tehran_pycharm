from django.urls import path
from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegistrationForm, LoginForm
from .models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout


def index(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request, 'login.html')

def signin(request):
    if request.method == 'POST':
        input_id = request.POST['id']
        input_password = request.POST['password']
        hashed_password = make_password(input_password)

        user = authenticate(request, id=input_id, password=input_password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = user.name
            request.session['id'] = user.id
            return redirect('/')
        else:
            messages.error(request, '유효하지 않은 로그인 정보입니다.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('/login_page/')

def register(request):
    return render(request, 'register.html')

def regist(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            hashed_password = make_password(password)

            user = User(id=id, password=hashed_password, email=email, name=name)
            user.save()

            # 회원가입이 완료되면 로그인 페이지로 리다이렉션
            return redirect('/login/')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def check_duplicate_id(request):
    if request.method == 'GET' and request.GET.get('id'):
        id = request.GET.get('id')
        data = {
            'is_taken': User.objects.filter(id=id).exists()
        }
        return JsonResponse(data)
    else:
        data = {
            'is_taken': False
        }
        return JsonResponse(data)
