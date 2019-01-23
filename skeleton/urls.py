from django.urls import path
from . import views

app_name = 'skeleton'

urlpatterns = [
    path('', views.skeleton_detail),
    path('<slug:year_slug>/', views.year_detail, name='year_detail'),
    path('<slug:year_slug>/<slug:team_slug>/', views.team_detail, name='team_detail'),
    path('<slug:year_slug>/<slug:team_slug>/<slug:player_slug>', views.player_detail, name='player_detail')
]
