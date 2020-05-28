from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from race_list_app.module import race_list as rl
import pandas as pd
import os
from datetime import datetime as dt
# Create your views here.

def racefunc(request):
    if not 'user_id' in request.session: return redirect('/auth/login')
    d = {
        'days_li': rl.Racedays(),
        'places': rl.Raceplace(),
        'races' : rl.Raceinfo(),
    }
    return render(request, 'race_list/race_list.html', d)