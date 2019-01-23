from django.urls import path
from . import views

app_name = 'area_team'

urlpatterns = [
    path('', views.home, name='home'),
    path('modify-players/', views.modify_players, name='modify_players'),
    path('modify-coaches/', views.modify_coaches, name='modify_coaches'),
    path('modify-team/', views.modify_team, name='modify_team'), ]
