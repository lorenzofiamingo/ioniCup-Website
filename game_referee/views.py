from django.shortcuts import render, redirect
from skeleton.models import Match


def referee(request):
    if request.method == "POST":
        match = Match.objects.get(id=request.POST.get('match_id'))
        playersA = []
        playersB = []
        coachesA = []
        coachesB = []

        temp = list(match.team_A.players.all())
        for player in temp:
            if player.jersey_number is None:
                player.jersey_number = 99999
        temp.sort(key=lambda x: x.jersey_number)
        for i in range(12):
            if temp and i < len(temp):
                playersA.append([temp[i], temp[i].jersey_number])
        for player in playersA:
            if player[1] == 99999:
                player[1] = ''

        temp = list(match.team_B.players.all())
        for player in temp:
            if player.jersey_number is None:
                player.jersey_number = 99999
        temp.sort(key=lambda x: x.jersey_number)
        for i in range(12):
            if temp and i < len(temp):
                playersB.append([temp[i], temp[i].jersey_number])
        for player in playersB:
            if player[1] == 99999:
                player[1] = ''

        temp = list(match.team_A.coaches.all())
        for i in range(2):
            if temp and i < len(temp):
                coachesA.append([temp[i], temp[i].cell_number])
        for coach in coachesA:
            if coach[1] is None:
                coach[1] = ''

        temp = list(match.team_B.coaches.all())
        for i in range(2):
            if temp and i < len(temp):
                coachesB.append([temp[i], temp[i].cell_number])
        for coach in coachesB:
            if coach[1] is None:
                coach[1] = ''

        num = match.number if match.number else ''
        court = match.court if match.court else ''

        params = {
            'match': match,
            'num': num,
            'court': court,
            'playersA': playersA,
            'playersB': playersB,
            'coachesA': coachesA,
            'coachesB': coachesB}

    else:
        params = dict()
    return render(request, 'game_referee/referee.html', params)
