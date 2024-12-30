from django.shortcuts import render
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import scoreboardv2

from datetime import datetime, timedelta

def verPartidos(request):
    board = scoreboard.ScoreBoard()
    result = board.games.get_dict()
    games=[]
    for item in result:
        equipoLocalNombre = item["homeTeam"]["teamCity"]+" "+item["homeTeam"]["teamName"]
        equipoVisitanteNombre = item["awayTeam"]["teamCity"]+" "+item["awayTeam"]["teamName"]
        puntosLocal = item["homeTeam"]["score"]
        puntosVisitante = item["awayTeam"]["score"]
        print(equipoLocalNombre)
        logoLocal = f'{equipoLocalNombre.replace(" ", "")}Logo.png'
        logoVisitante = f'{equipoVisitanteNombre.replace(" ", "")}Logo.png'
        games.append({
            "equipoLocalNombre" : equipoLocalNombre,
            "equipoVisitanteNombre" : equipoVisitanteNombre,
            "puntosLocal" : puntosLocal,
            "puntosVisitante" : puntosVisitante,
            "logoLocal" : logoLocal,
            "logoVisitante" : logoVisitante
        })
    return render(request, 'index.html', {'games':games})

def verPartidosManana(request):

    manana = datetime.now() + timedelta(days=1)
    manana = manana.strftime('%Y-%m-%d')

    scoreboard = scoreboardv2.ScoreboardV2(game_date=manana)

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

    return render(request,"manana.html",{"mapaPartidos": mapaPartidos,"fecha":manana})

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



