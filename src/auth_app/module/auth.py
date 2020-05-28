from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..forms import LoginForm, RegisterForm
from ..models import Users
from hashlib import sha1
import datetime

""" 新規登録チェック """
def CreateAdminUser(request, Data):
    # もし、メールアドレスが既に登録されていたらエラーを返す
    if Users.objects.filter(email = Data['email']):
        url = ''
    else:
        # ここで新規登録処理
        now = datetime.datetime.now()
        UserData = Users(
            name = Data['name'],
            email = Data['email'],
            password = sha1(Data['password'].encode('utf-8')).hexdigest(),
            status = 2,
            created_at = now,
        )
        UserData.save()
        user = Users.objects.all().filter(name = Data['name']).first()
        request.session['user_id'] = user.email
        url = '/race_list'

    return url

""" ログインチェック """
def Login(request, Data):
    user = Users.objects.all().filter(email = Data['email']).first()
    password = sha1(Data['password'].encode('utf-8')).hexdigest()
    if user and password == user.password:
        request.session['user_id'] = user.id
        request.session['redirect_flag'] = 0
        request.session['redirect_delete_flag'] = 0
        url = '/race_list'
    else:
        url = ''

    return url
