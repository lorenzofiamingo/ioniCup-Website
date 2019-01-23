from django.urls import path
from . import views

app_name = 'area_master'

urlpatterns = [
    path('', views.home, name='home'),
    path('update-groups/', views.update_groups, name='update_groups'),
    path('modify-groups/', views.modify_groups, name='modify_groups'),
    path('modify-stages/', views.modify_stages, name='modify_stages'),
    path('modify-scores/', views.modify_scores, name='modify_scores'),
    path('delete-scores/', views.delete_scores, name='delete_scores'),
    path('modify-times/', views.modify_times, name='modify_times'),
    path('update-matches/', views.update_matches, name='update_matches'),
    path('delete-rounds/', views.delete_rounds, name='delete_rounds'), ]
