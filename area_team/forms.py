from skeleton.models import Player, Coach, Team
from django.forms import ModelForm


class PlayerForm(ModelForm):

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'jersey_number', 'year_of_birth', 'all_star_game']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Cognome',
            'jersey_number': 'Numero di maglia',
            'year_of_birth': 'Anno di  nascita', }



class CoachForm(ModelForm):

    class Meta:
        model = Coach
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Cognome', }


class TeamForm(ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'short_name', 'city', 'color']
        labels = {
            'name': 'Denominazione ufficiale',
            'short_name': 'Denominazione corta (max 12 caratteri)',
            'city': 'Città',
            'color': 'Colore della divisa', }
