from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms import modelform_factory
from django.shortcuts import render, redirect, HttpResponse
from skeleton.models import Match
from .forms import MatchForm

from django.core.serializers import serialize
import pusher


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_master or u.is_superuser)
def edit(request, match_number):
    match = Match.objects.get(number=match_number)
    MatchFormOne = modelform_factory(Match, form=MatchForm)
    if request.method == "POST":
        match_form = MatchFormOne(request.POST, request.FILES, instance=match)
        if match_form.is_valid():
            match_form.save()
            if request.POST.get('button') == '':
                return redirect('area_scorekeeper:home')

            match = Match.objects.get(number=match_number)
            json_match = type(match).objects.filter(pk=match.pk).values().first()  # convert match to JSON
            json_match.update({'get_sb_current_sixth_display': match.get_sb_current_sixth_display()})
            pusher_client = pusher.Pusher(app_id='699949', key='f7d3abbadd2b734a4493', secret='f9ca67596626dd8a452c', cluster='eu', ssl=True)
            pusher_client.trigger(str(match_number), 'match_is_updated', json_match)

    else:
        match_form = MatchFormOne(instance=match)
    return render(request, 'game_scoreboard/edit_scoreboard.html', {'match': match, 'match_form': match_form})


def show(request, match_number):
    match = Match.objects.get(number=match_number)
    return render(request, 'game_scoreboard/show_scoreboard.html', {'match': match, })
