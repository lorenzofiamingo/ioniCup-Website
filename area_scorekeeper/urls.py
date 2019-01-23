from django.urls import path
from . import views

app_name = 'area_scorekeeper'

urlpatterns = [
    path('', views.home, name='home'), ]
