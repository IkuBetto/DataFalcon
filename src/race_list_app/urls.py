from django.urls import path, include
from . import views

app_name = 'race_list'

urlpatterns = [
    path('', views.racefunc, name='race'),
]