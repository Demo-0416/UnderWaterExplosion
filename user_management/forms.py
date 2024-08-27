from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单
class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


# 修改密码提交的表单
class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    repeat_password = forms.CharField()
