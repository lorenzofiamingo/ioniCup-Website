from django.urls import path
from . import views

app_name = 'game_referee'

urlpatterns = [
    path('referee/', views.referee, name='referee'), ]
