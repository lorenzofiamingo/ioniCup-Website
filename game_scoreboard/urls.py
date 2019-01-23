from django.urls import path
from . import views

app_name = 'game_scoreboard'

urlpatterns = [
    path('edit/<int:match_number>', views.edit, name='edit'),
    path('show/<int:match_number>', views.show, name='show'), ]
