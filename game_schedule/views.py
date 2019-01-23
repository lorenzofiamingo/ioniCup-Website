from django.shortcuts import render, redirect
from skeleton.models import Tournament, Match, Court, Time, Day


def isListEmpty(inList):
    if isinstance(inList, list):
        return all(map(isListEmpty, inList))
    return False


def schedule(request):
    if request.method == "POST":
        tournament = Tournament.objects.get(id=request.POST.get('tournament_id'))
        matches = []
        times = []

        # qui si mettono le partite in liste
        for stage in tournament.stages.all():
            temp_groups = []
            for group in stage.groups.all():
                temp_rounds = []
                for round in group.rounds.all():
                    temp_matches = []
                    for match in round.matches.all():
                        temp_matches.append(match)
                    temp_rounds.append(temp_matches)
                temp_groups.append(temp_rounds)
            # qui si mettono le partite in ordine
            test = temp_groups
            while not isListEmpty(temp_groups):
                for group in temp_groups:
                    for match in group[0]:
                        matches.append(match)
                    group.pop(0)

        # qui si assegnano tempi, campi e numeri alle partite
        try:
            time = Time.objects.get(initial=True)
        except Time.DoesNotExist:
            time = None
        num = 1
        courts = list(Court.objects.all())
        courts.sort(key=lambda x: x.importance, reverse=True)
        while time:
            if time.event is '':
                for court in courts:
                    if matches:
                        if not matches[0].number:
                            matches[0].number = num
                        if not matches[0].court:
                            matches[0].court = court
                        if not matches[0].time:
                            matches[0].time = time
                        matches[0].save()
                        matches.pop(0)
                        num += 1
            times.append(time)
            try:
                time = time.next_time
            except Time.DoesNotExist:
                time = None

        params = {'times': times}

    else:
        params = dict()
    return render(request, 'game_schedule/schedule.html', params)
