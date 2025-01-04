from django.shortcuts import render
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import scoreboardv2
from nba_api.live.nba.endpoints import boxscore

from datetime import datetime, timedelta

import pytz
from django.utils import timezone
from datetime import datetime, timedelta

def verPartidos(request):
    zona_horaria_argentina = pytz.timezone('America/Buenos_Aires')
    board = scoreboard.ScoreBoard()
    result = board.games.get_dict()
    games={}
    fecha=datetime.now()
    condicion= fecha.strftime("%Y-%m-%d")
    print(fecha.strftime("%H"))
    print (board.score_board_date)
    if (board.score_board_date == condicion) | (fecha.strftime("%H") <= "03"):
        for item in result:
            equipoLocalNombre = item["homeTeam"]["teamCity"]+" "+item["homeTeam"]["teamName"]
            equipoVisitanteNombre = item["awayTeam"]["teamCity"]+" "+item["awayTeam"]["teamName"]
            puntosLocal = item["homeTeam"]["score"]
            puntosVisitante = item["awayTeam"]["score"]
            logoLocal = f'{equipoLocalNombre.replace(" ", "")}Logo.png'
            logoVisitante = f'{equipoVisitanteNombre.replace(" ", "")}Logo.png'
            id_partido = item['gameId']
            horario = item['gameTimeUTC']
            horario = datetime.fromisoformat(horario.replace('Z', '+00:00'))
            horario = horario.replace(tzinfo=pytz.utc)
            horario = horario.astimezone(zona_horaria_argentina)
            fecha_argentina= horario.strftime('%H:%M')
            games[id_partido]= {
                "equipo1" : equipoLocalNombre,
                "equipo2" : equipoVisitanteNombre,
                "puntos1" : puntosLocal,
                "puntos2" : puntosVisitante,
                "equipo1Logo" : logoLocal,
                "equipo2Logo" : logoVisitante,
                "fecha_argentina": fecha_argentina,
            }
    else:
        games = obtenerFecha(fecha)
        
    return render(request, 'index.html', {'games':games})

def obtenerFecha(fecha:datetime):
    fecha = fecha.strftime('%Y-%m-%d')

    scoreboard = scoreboardv2.ScoreboardV2(game_date=fecha)

    partidosDict = scoreboard.get_dict()

    recorte = partidosDict["resultSets"][1]["rowSet"]

    mapaPartidos = {}

    for partido in recorte:
        id_partido = partido[2]
        equipo = partido[5]+" "+partido[6]
        if partido[22] != None:
            puntos = partido[22]
        else:
            puntos=0
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
                "equipo2Logo" : None,
            }
        else:
            # Si ya existe, completamos los datos faltantes
            if mapaPartidos[id_partido]["equipo2"] is None:
                mapaPartidos[id_partido]["equipo2"] = equipo
                mapaPartidos[id_partido]["puntos2"] = puntos
                mapaPartidos[id_partido]["equipo2Logo"] = logo
    return mapaPartidos

def verPartidosManana(request):

    manana = datetime.now() + timedelta(days=1)
    fecha = manana.strftime('%Y-%m-%d')
    mapaPartidos= obtenerFecha(manana)
    return render(request,"manana.html",{"mapaPartidos": mapaPartidos,"fecha":fecha})

def verPartidosAyer(request):

    ayer = datetime.now() - timedelta(days=1)
    fecha = ayer.strftime('%Y-%m-%d')
    mapaPartidos=obtenerFecha(ayer)
    return render(request,"ayer.html",{"mapaPartidos": mapaPartidos,"fecha":fecha})

def informacionDetalladaPartido(request,idPartido):
    boxScoreInit = boxscore.BoxScore(idPartido)
    datos = boxScoreInit.get_dict()
    return render(request,"partidoDetalle.html",{"datos":datos})




