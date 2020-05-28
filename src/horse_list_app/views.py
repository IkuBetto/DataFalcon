from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from horse_list_app.module import horse_list as hl
from race_list_app.module import race_list as rl
import pandas as pd
import os
from datetime import datetime as dt
import urllib
import csv

# Create your views here.

# レース別馬情報のビュー
def raceHorsefunc(request):
    if not 'user_id' in request.session:
        return redirect('/auth/login')
    raceinfo = request.GET.get('raceinfo')
    date, place, num, name = raceinfo.split(',')
    horselist = hl.HorseList(date, place, num)
    if 'horseinfo' in request.session:
        del request.session['horseinfo']
    request.session['horseinfo'] = horselist
    d = {
        'name' : dt.strptime(date, '%Y_%m_%d').strftime('%-m月%-d日') + "　" + place +"競馬場　" + num + "　" +name,
        'horses' : horselist,
    }
    return render(request, 'horse_list/horse_list.html', d)

# 全馬情報のビュー
def allHorsefunc(request):
    if not 'user_id' in request.session:
        return redirect('/auth/login')
    date = request.GET.get('date_of_race',hl.firstDate())
    sort = request.GET.get('sort')
    rankto = request.GET.get('rankto','')
    rankfrom = request.GET.get('rankfrom','')
    horselist = hl.HorseSort(date, sort, rankto, rankfrom)
    if 'horseinfo' in request.session:
        del request.session['horseinfo']
    request.session['horseinfo'] = horselist
    d = {
        'horses': horselist,
        'days_li': rl.Racedays(),
        'sort' : sort,
        'rankto':rankto,
        'rankfrom':rankfrom,
        'date_of_race': date,
    }

    return render(request, 'horse_list/horse_for_race.html', d)

# レース別馬情報のエクスポート
def exportInfo(request):
    if not 'user_id' in request.session:
        return redirect('/auth/login')
    horselist = request.session['horseinfo']
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    filename = urllib.parse.quote((u'horses_in_race.csv').encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    writer = csv.writer(response)
    header = ["","日付","場所","レースNo","レース名","馬名","1走前レース名","2走前レース名","3走前レース名","4走前レース名","5走前レース名","1走前着順","2走前着順","3走前着順","4走前着順","5走前着順","1走前頭数","2走前頭数","3走前頭数","4走前頭数","5走前頭数","1走前上位馬平均順位","2走前上位馬平均順位","3走前上位馬平均順位","4走前上位馬平均順位","5走前上位馬平均順位","1走前下位馬平均順位","2走前下位馬平均順位","3走前下位馬平均順位","4走前下位馬平均順位","5走前下位馬平均順位"]
    writer.writerow(header)
    for i in range(len(horselist)):
        writer.writerow([i+1] + horselist[i][:30])
    return response

# 全馬情報のエクスポート
# 場所とレース名は今後実装する
def exportAll(request):
    if not 'user_id' in request.session:
        return redirect('/auth/login')
    horselist = request.session['horseinfo']
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    filename = urllib.parse.quote((u'all_horses.csv').encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    writer = csv.writer(response)
    header = ["","日付","場所","レースNo","レース名","馬名","過去レース名","過去レース着順","過去レース頭数","上位馬の次走平均順位","下位馬の次走平均順位","過去レース"]
    writer.writerow(header)
    for index in range(len(horselist)):
        writer.writerow([index+1] + horselist[index])
    return response