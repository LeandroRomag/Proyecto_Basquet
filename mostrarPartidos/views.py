from django.shortcuts import render
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import scoreboardv2

from datetime import datetime, timedelta
import json

# Create your views here.
def verPartidos(request):
    DatosEnJson = scoreboard.ScoreBoard().games.get_json()
    data = json.loads(DatosEnJson)
    return render(request, 'index.html', {
        'games':data})

def verPartidosAyer(request):

    ayer = datetime.now() - timedelta(days=1)
    ayer = ayer.strftime('%Y-%m-%d')

    scoreboard = scoreboardv2.ScoreboardV2(game_date=ayer)

    partidosDict = scoreboard.get_dict()

    recorte = partidosDict["resultSets"][1]["rowSet"]

    mapaPartidos = {}

    for partido in recorte:
        id_partido = partido[2]
        equipo = partido[5]+" "+partido[6]
        puntos = partido[22]
        logo = f'{equipo.replace(" ", "")}Logo.png'

        # Si el ID del partido no existe, inicializamos con los datos actuales
        if id_partido not in mapaPartidos:
            mapaPartidos[id_partido] = {
                "equipo1": equipo,
                "puntos1": puntos,
                "equipo1Logo" : logo,
                "equipo2": None,
                "puntos2": None,
                "equipo2Logo" : None,
                "escudoEquipo2" : None,
            }
        else:
            # Si ya existe, completamos los datos faltantes
            if mapaPartidos[id_partido]["equipo2"] is None:
                mapaPartidos[id_partido]["equipo2"] = equipo
                mapaPartidos[id_partido]["puntos2"] = puntos
                mapaPartidos[id_partido]["equipo2Logo"] = logo
    
    return render(request,"ayer.html",{"mapaPartidos": mapaPartidos,"fecha":ayer})

