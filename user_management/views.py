from django.shortcuts import render, redirect
from django.http import HttpResponse
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
                return redirect('home')  # 登录后定向待定
            else:
                return HttpResponse("账号或密码有误")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 用户登出
def user_logout(request):
    logout(request)
    return redirect('')  # 登出后定向待定


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回页面
            login(request, new_user)
            return redirect('home')  # 注册后直接登录，定向待定
        else:
            return HttpResponse("注册表单输入有误")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


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
def user_change_password(request):
    state = None
    if request.method == 'POST':
        user = request.user
        user_change_password_form = UserChangePasswordForm(request.POST)
        if user_change_password_form.is_valid():
            old_password = user_change_password_form.cleaned_data['old_password']
            new_password = user_change_password_form.cleaned_data['new_password']
            repeat_password = user_change_password_form.cleaned_data['repeat_password']
            if user.check_password(old_password):
                if not new_password:
                    state = 'empty'
                    return HttpResponse("新密码为空")
                elif new_password != repeat_password:
                    state = 'repeat_error'
                    return HttpResponse("密码输入不一致")
                else:
                    user.set_password(new_password)
                    user.save()
                    state = 'success'
                    logout(request)
                    return redirect('userprofile:login')
            else:
                state = 'password_error'
                return HttpResponse("密码错误")
    elif request.method == 'GET':
        user_change_password_form = UserChangePasswordForm()
        context = {'form': user_change_password_form}
        return render(request, 'user/change_password.html', context)