from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms import modelform_factory
from django.shortcuts import render, redirect
from skeleton.models import Match
from .forms import MatchForm
from django.utils.safestring import mark_safe
import json


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def edit(request, match_number):
    match = Match.objects.get(number=match_number)
    MatchFormOne = modelform_factory(Match, form=MatchForm)
    if request.method == "POST":
        match_form = MatchFormOne(request.POST, request.FILES, instance=match)
        if match_form.is_valid():
            match_form.save()
            if request.POST.get('button') == 'Esci':
                return redirect('area_scorekeeper:home')
    else:
        match_form = MatchFormOne(instance=match)
    return render(request, 'game_scoreboard/edit_scoreboard.html', {'match': match, 'match_form': match_form})


def show(request, match_number):
    match = Match.objects.get(number=match_number)
    return render(request, 'game_scoreboard/show_scoreboard.html', {'match': match, })
