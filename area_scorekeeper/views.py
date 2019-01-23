from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from skeleton.models import Match, Tournament


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.is_scorekeeper or u.is_superuser)
def home(request):
    try:
        tournament = Tournament.objects.get(active=True)
    except Tournament.DoesNotExist:
        return render(request, 'area_scorekeeper/base_layout.html')
    matches = []
    for stage in tournament.stages.all():
        for group in stage.groups.all():
            for round in group.rounds.all():
                for match in round.matches.all():
                    matches.append(match)
    matches.sort(key=lambda x: x.number)
    return render(request, 'area_scorekeeper/home.html', {'matches': matches})
