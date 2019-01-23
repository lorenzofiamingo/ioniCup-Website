from django.shortcuts import render, redirect
from skeleton.models import Team, Player, Coach
from django.contrib.auth.decorators import login_required
from .forms import PlayerForm, CoachForm, TeamForm
from django.forms import modelformset_factory, modelform_factory
from django.http import HttpResponseNotFound


# Create your views here.
@login_required(login_url="/accounts/login/")
def home(request):
    if request.user.team:
        team = request.user.team
        players = team.players.all()
        coaches = team.coaches.all()
        return render(request, 'area_team/home.html', {'players': players, 'coaches': coaches, 'team': team})
    else:
        return render(request, 'area_team/base_layout.html')


@login_required(login_url="/accounts/login/")
def modify_players(request):
    if request.user.team:
        PlayerFormSet = modelformset_factory(Player, form=PlayerForm, extra=1, can_delete=True,)

        if request.method == "POST":
            player_formset = PlayerFormSet(request.POST, request.FILES, queryset=request.user.team.players.all())
            for player_form in player_formset:
                if player_form.is_valid():
                    player = player_form.save(commit=False)
                    player.team = request.user.team
            if player_formset.is_valid():
                player_formset.save()
                if request.POST.get('button') == 'Salva ed esci':
                    return redirect('area_team:home')
                else:
                    return redirect('area_team:modify_players')
        else:
            player_formset = PlayerFormSet(queryset=request.user.team.players.all())
        return render(request, 'area_team/modify_players.html', {'player_formset': player_formset})
    else:
        return redirect('area_team:home')


@login_required(login_url="/accounts/login/")
def modify_coaches(request):
    if request.user.team:
        CoachFormSet = modelformset_factory(Coach, form=CoachForm, extra=1, can_delete=True,)

        if request.method == "POST":
            coach_formset = CoachFormSet(request.POST, request.FILES, queryset=request.user.team.coaches.all())
            for coach_form in coach_formset:
                if coach_form.is_valid():
                    coach = coach_form.save(commit=False)
                    coach.team = request.user.team
            if coach_formset.is_valid():
                coach_formset.save()
                if request.POST.get('button') == 'Salva ed esci':
                    return redirect('area_team:home')
                else:
                    return redirect('area_team:modify_coaches')
        else:
            coach_formset = CoachFormSet(queryset=request.user.team.coaches.all())
        return render(request, 'area_team/modify_coaches.html', {'coach_formset': coach_formset})
    else:
        return redirect('area_team:home')


@login_required(login_url="/accounts/login/")
def modify_team(request):
    if request.user.team:
        TeamFormOne = modelform_factory(Team, form=TeamForm)

        if request.method == "POST":
            team_form = TeamFormOne(request.POST, request.FILES, instance=request.user.team)
            if team_form.is_valid():
                team_form.save()
                if request.POST.get('button') == 'Salva ed esci':
                    return redirect('area_team:home')
                else:
                    return redirect('area_team:modify_team')
        else:
            team_form = TeamFormOne(instance=request.user.team)
        return render(request, 'area_team/modify_team.html', {'team_form': team_form})
    else:
        return redirect('area_team:home')
