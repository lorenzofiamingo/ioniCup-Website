from skeleton.models import Match
from django.forms import ModelForm


class MatchForm(ModelForm):

    class Meta:
        model = Match
        exclude = [
            'round',
            'team_A',
            'team_B',
            'time',
            'court',
            'number', ]
