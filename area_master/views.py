from django.shortcuts import render, redirect
from skeleton.models import *
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from django.forms import modelform_factory, modelformset_factory
from django.http import HttpResponse
from itertools import zip_longest
from math import log


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def home(request):
    try:
        tournament = Tournament.objects.get(active=True)
    except:
        return render(request, 'area_master/base_layout.html')

    return render(request, 'area_master/home.html', {'tournament': tournament, })


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def modify_groups(request):
    GroupFormSet = modelformset_factory(Group, form=GroupForm, extra=1, can_delete=True,)
    if request.method == "POST":
        group_formset = GroupFormSet(request.POST, request.FILES, queryset=Group.objects.filter(stage=request.GET.get('stage_id')))
        if group_formset.is_valid():
            group_formset.save()
            if request.POST.get('button') == 'Salva ed esci':
                return redirect('area_master:home')
    group_formset = GroupFormSet(queryset=Group.objects.filter(stage=request.GET.get('stage_id')))
    return render(request, 'area_master/modify_groups.html', {'group_formset': group_formset})


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def modify_stages(request):
    StageFormSet = modelformset_factory(Stage, form=StageForm, extra=1, can_delete=True,)
    if request.method == "POST":
        stage_formset = StageFormSet(request.POST, request.FILES, queryset=Stage.objects.filter(tournament=request.GET.get('tournament_id')))
        if stage_formset.is_valid():
            stage_formset.save()
            if request.POST.get('button') == 'Salva ed esci':
                return redirect('area_master:home')
    stage_formset = StageFormSet(queryset=Stage.objects.filter(tournament=request.GET.get('tournament_id')))
    return render(request, 'area_master/modify_stages.html', {'stage_formset': stage_formset})


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def update_groups(request):
    if request.method == 'POST':
        stage = Stage.objects.get(id=request.POST.get('stage_id'))
        if stage.protected:
            return redirect('area_master:home')
        current_groups = []
        precedent_groups = []
        leader_boards = []
        temp = []
        rank = []

        for group in stage.precedent_stage.groups.all():
            leader_board = []
            for score in group.scores.all():
                leader_board.append(score)
            leader_board.sort(key=lambda x: x.score, reverse=True)  # ordina le migliori nel girone...
            leader_boards.append(leader_board)

        leader_boards = [list(filter(None, i)) for i in zip_longest(*leader_boards)]  # trasporta leader_boards
        for leader_board in leader_boards:
            leader_board.sort(key=lambda x: x.score, reverse=True)  # ordina le migliori prime, seconde, terze...
            for score in leader_board:
                temp.append(score)

        temp.sort(key=lambda x: x.group.importance, reverse=True)  # ordina per importanza del girone precedente
        for score in temp:
            rank.append(score.team)

        for group in stage.groups.all():
            current_groups.append(group)
        current_groups.sort(key=lambda x: x.importance, reverse=True)

        i = 0
        t = 1
        while len(rank) and len(current_groups):
            if len(current_groups[i].scores.all()) < current_groups[i].number_of_teams:
                Score.objects.get_or_create(team=rank[0], group=current_groups[i])
                rank.pop(0)
            if i+t < 0 or i+t >= len(current_groups) or current_groups[i+t].importance is not current_groups[i].importance:
                t = -1 if t == 1 else 1
                if len(current_groups[i].scores.all()) == current_groups[i].number_of_teams:
                    rem = current_groups[i].importance
                    current_groups.pop(i)
                    if t == 1:
                        i -= 1
                    elif i < len(current_groups) and rem is not current_groups[i].importance:
                        t = 1
                    elif len(current_groups) == 1:
                        i = 0
            else:
                i += t
                if len(current_groups[i].scores.all()) >= current_groups[i].number_of_teams:
                    current_groups.pop(i)
                    if t == 1:
                        i -= 1

        return redirect('area_master:home')


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def modify_scores(request):
    ScoreFormSet = modelformset_factory(Score, form=ScoreForm, extra=1, can_delete=True,)
    if request.method == "POST":
        score_formset = ScoreFormSet(request.POST, request.FILES, queryset=Score.objects.filter(group=request.GET.get('group_id')))
        if score_formset.is_valid():
            score_formset.save()
            if request.POST.get('button') == 'Salva ed esci':
                return redirect('area_master:home')
    score_formset = ScoreFormSet(queryset=Score.objects.filter(group=request.GET.get('group_id')))
    return render(request, 'area_master/modify_scores.html', {'score_formset': score_formset})


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def delete_scores(request):
    if request.method == "POST":
        Score.objects.filter(group=request.POST.get('group_id')).delete()
    return redirect('area_master:home')


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def update_matches(request):
    if request.method == 'POST':
        group = Group.objects.get(id=request.POST.get('group_id'))
        scores = list(group.scores.all())
        if group.format == 'Round-Robin':
            if len(scores) % 2:
                scores.append(None)
            n = int(len(scores)/2)
            for r in range(1, 2*n):
                round = Round.objects.get_or_create(round=r, group=group)[0]
                for i in range(n):
                    if scores[i] and scores[2*n - 1 - i]:
                        Match.objects.get_or_create(round=round, team_A=scores[i].team, team_B=scores[2*n - 1 - i].team)
                scores.insert(1, scores.pop())
        if group.format == 'Elimination':
            while not (len(scores) > 1 and not len(scores) & (len(scores) - 1)):
                scores.append(None)
            scoreboard = []
            scoreboard.append(scores)
            Team.objects.filter(tournament=None).delete()

            for r in range(1, int(log(len(scores), 2)) + 1):
                round = Round.objects.get_or_create(round=r, group=group)[0]
                new_scoreboard = []
                for bounch in scoreboard:
                    los_scores = []
                    win_scores = []
                    for i in range(int(len(bounch)/2)):
                        if bounch[i] is not None and bounch[-1-i] is not None:
                            match = Match.objects.get_or_create(round=round, team_A=bounch[i].team, team_B=bounch[-1-i].team)[0]
                            if match.points_A and match.points_B and match.points_A > match.points_B:
                                win_scores.append(bounch[i])
                                los_scores.append(bounch[-1-i])
                            elif match.points_A and match.points_B and match.points_A < match.points_B:
                                win_scores.append(bounch[-1-i])
                                los_scores.append(bounch[i])
                            else:
                                win_team = Team.objects.get_or_create(name='vincitrice tra (%s) e (%s)' % (match.team_A, match.team_B), tournament=None)[0]
                                win_scores.append(Score.objects.get_or_create(team=win_team)[0])
                                los_team = Team.objects.get_or_create(name='sconfitto tra (%s) e (%s)' % (match.team_A, match.team_B), tournament=None)[0]
                                los_scores.append(Score.objects.get_or_create(team=los_team)[0])
                        elif bounch[i]:
                            win_scores.append(bounch[i])
                            los_scores.append(None)
                        elif bounch[1-i]:
                            win_scores.append(bounch[-1-i])
                            los_scores.append(None)
                        else:
                            win_scores.append(None)
                            los_scores.append(None)
                    new_scoreboard.append(win_scores)
                    new_scoreboard.append(los_scores)
                scoreboard = new_scoreboard

        return redirect('area_master:home')


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def delete_rounds(request):
    if request.method == "POST":
        Round.objects.filter(group=request.POST.get('group_id')).delete()
    return redirect('area_master:home')


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def modify_times(request):
    TimeFormSet = modelformset_factory(Time, form=TimeForm, extra=1, can_delete=True,)
    DayFormSet = modelformset_factory(Day, form=DayForm, extra=1, can_delete=True,)
    if request.method == "POST":
        time_formset = TimeFormSet(request.POST, request.FILES, queryset=Time.objects.all())
        day_formset = DayFormSet(request.POST, request.FILES, queryset=Day.objects.all())
        if time_formset.is_valid() or day_formset.is_valid():
            if time_formset.is_valid():
                time_formset.save()
            if day_formset.is_valid():
                day_formset.save()
            if request.POST.get('button') == 'Salva ed esci':
                return redirect('area_master:home')
    time_formset = TimeFormSet(queryset=Time.objects.all())
    day_formset = DayFormSet(queryset=Day.objects.all())
    return render(request, 'area_master/modify_times.html', {'time_formset': time_formset, 'day_formset': day_formset})
