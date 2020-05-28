from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from hashlib import sha1
from .forms import LoginForm, RegisterForm
from .models import Users
from .module import auth
import sys
import datetime

# Create your views here.

""" 新規登録 """
def register(request):
    # ステータス 2 のユーザーをマスタユーザーとする
    # マスタユーザーがいた場合は、ここからアカウント追加は出来ないようにする
    if Users.objects.all().filter(status = 2).first():
        return redirect('/auth/login')

    RegisterFormData = RegisterForm()
    return render(request, 'auth/register.html', {'form': RegisterFormData})

def create(request):
    RegisterFormData = RegisterForm(request.POST or None)
    # バリデーションチェック
    if RegisterFormData.is_valid():
        Data = RegisterFormData.cleaned_data
        # 登録されているか確認
        url = auth.CreateAdminUser(request, Data)
        if not url:
            RegisterFormData = RegisterForm()
            data = {
                'form': RegisterFormData,
                'error': 'このメールアドレスは既に登録されています。',
            }

            return render(request, 'auth/register.html', data)
    else:
        # バリデーションエラーはこっち
        url = '/auth/register'

    return redirect(url)
""" ここまで新規登録 """

""" ログイン """
def login(request):
    LoginFormData = LoginForm(request.POST or None)

    # バリデーションチェック
    if LoginFormData.is_valid():
        Data = LoginFormData.cleaned_data
        # 登録されているかチェック
        url = auth.Login(request, Data)
        if not url:
            # 登録されていなかったらエラーを返す
            data = {
                'form': LoginFormData,
                'error': 'メールアドレスまたはパスワードが違います。',
            }

            return render(request, 'auth/login.html', data)
    else:
        # バリデーションエラーはこっち
        return render(request, 'auth/login.html', {'form': LoginFormData})

    # 登録されていれば、一覧画面にリダイレクト
    return redirect(url)

""" ログアウト（まだ未実装） """
def logout(request):
    request.session.clear()
    LoginFormData = LoginForm()
    return render(request, 'auth/login.html', {'form': LoginFormData})