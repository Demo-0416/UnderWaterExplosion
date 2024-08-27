from django.shortcuts import render, redirect
<<<<<<< HEAD
from django.http import HttpResponse, JsonResponse
=======
from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
>>>>>>> 4b57c3c (接口跨域更改设置)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm, UserChangePasswordForm

# Create your views here.
# 用户登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('data_management: home')  # 登录后定向待定
            else:
                return JsonResponse({'code': '1', 'state': '账号或密码有误'})
        else:
            return JsonResponse({'code': '2', 'state': '账号或密码输入不合法'})
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'login.html', context)
    else:
        return JsonResponse({'code': '2', 'state': '请使用GET或POST请求数据'})


# 用户登出
def user_logout(request):
    logout(request)
    return redirect('data_management: home')  # 登出后定向待定


# 用户注册
@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登录用户
            # 可以重定向到首页或其他页面
            return redirect('data_management: home') # 定向待定
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# 用户删除
@login_required(login_url='/user_management/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('user_management:login')
        else:
            return HttpResponse("你没有操作权限")
    else:
        return HttpResponse("仅接受POST请求")


# 用户修改密码
@login_required(login_url='/user_management/login/')
def change_password(request):
    if request.method == 'POST':
        user = request.user
        user_change_password_form = UserChangePasswordForm(request.POST)
        if user_change_password_form.is_valid():
            old_password = user_change_password_form.cleaned_data['old_password']
            new_password = user_change_password_form.cleaned_data['new_password']
            repeat_password = user_change_password_form.cleaned_data['repeat_password']
            if user.check_password(old_password):
                if new_password != repeat_password:
                    return JsonResponse({'code': '2', 'state': '密码输入不一致'})
                else:
                    user.set_password(new_password)
                    user.save()
                    logout(request)
                    return redirect('userprofile:login')
            else:
                return JsonResponse({'code': '3', 'state': '原密码错误'})
        else:
            return JsonResponse({'code': '1', 'state': '输入不能为空'})
    elif request.method == 'GET':
        user_change_password_form = UserChangePasswordForm()
        context = {'form': user_change_password_form}
        return render(request, 'change_password.html', context)