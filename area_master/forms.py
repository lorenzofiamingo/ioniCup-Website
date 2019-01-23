from skeleton.models import Stage, Group, Score, Time, Day
from django.forms import ModelForm


class StageForm(ModelForm):

    class Meta:
        model = Stage
        fields = '__all__'
        labels = {
            'name': 'nome',
            'tournament': 'torneo'}

class GroupForm(ModelForm):

    class Meta:
        model = Group
        fields = '__all__'
        labels = {
            'name': 'nome',
            'stage': 'fase',
            'format': 'formula'}


class ScoreForm(ModelForm):

    class Meta:
        model = Score
        fields = '__all__'
        labels = {
            'name': 'nome',
            'tournament': 'torneo'}

class TimeForm(ModelForm):

    class Meta:
        model = Time
        fields = '__all__'
        labels = {
            'name': 'nome',
            'tournament': 'torneo'}

class DayForm(ModelForm):

    class Meta:
        model = Day
        fields = '__all__'
        labels = {
            'name': 'nome',
            'tournament': 'torneo'}
