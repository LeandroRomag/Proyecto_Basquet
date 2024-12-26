from django.shortcuts import render
from nba_api.live.nba.endpoints import scoreboard
import json
# Create your views here.
def verPartidos(request):
    DatosEnJson = scoreboard.ScoreBoard().games.get_json()
    data = json.loads(DatosEnJson)
    return render(request, 'index.html', {
        'games':data})