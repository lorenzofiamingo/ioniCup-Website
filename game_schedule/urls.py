from django.urls import path
from . import views

app_name = 'game_schedule'

urlpatterns = [
    path('schedule/', views.schedule, name='schedule'), ]
