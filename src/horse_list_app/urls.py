from django.urls import path, include
from . import views

app_name = 'horse_list'

urlpatterns = [
    path('', views.raceHorsefunc, name='horse_for_race'),
    path('all', views.allHorsefunc, name='horse_of_all'),
    path('export', views.exportInfo, name='export'),
    path('export_all', views.exportAll, name='export_all'),
]