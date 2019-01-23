from django.shortcuts import render
from .models import Tournament, Team, Player


# Create your views here.
def skeleton_detail(request):
    years = Tournament.objects.all().order_by('year')
    return render(request, 'skeleton/skeleton_detail.html', {'years': years})


def year_detail(request, year_slug):
    year = Tournament.objects.get(slug=year_slug)
    teams = Team.objects.all().filter(year=year)
    return render(request, 'skeleton/year_detail.html', {'year': year, 'teams': teams})


def team_detail(request, year_slug, team_slug):
    year = Tournament.objects.get(slug=year_slug)
    team = Team.objects.get(slug=team_slug)
    players = Player.objects.all().filter(team=team)
    return render(request, 'skeleton/team_detail.html', {'year': year, 'team': team, 'players': players})


def player_detail(request, year_slug, team_slug, player_slug):
    year = Tournament.objects.get(slug=year_slug)
    team = Team.objects.get(slug=team_slug, year=year)
    player = Player.objects.get(slug=player_slug, team=team)
    return render(request, 'skeleton/player_detail.html', {'year': year, 'team': team, 'player': player})
