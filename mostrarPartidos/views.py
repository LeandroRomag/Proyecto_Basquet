from django.shortcuts import render
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import scoreboardv2
<<<<<<< HEAD

from datetime import datetime, timedelta
import json
import wikipedia



=======
from datetime import datetime, timedelta
from nba_api.stats.static import teams
from datetime import date
>>>>>>> leandro
# Create your views here.
f = "{gameId}: {awayTeam} {score1} vs. {score2} {homeTeam}"
team_dict = {team["id"]: team["full_name"] for team in teams.get_teams()}
def verPartidos(request):
    board = scoreboard.ScoreBoard()
    result = board.games.get_dict()
    print (result)
    games=[]
    for item in result:
        games.append(f.format(gameId=item['gameId'], awayTeam=item['awayTeam']['teamName'], score1=item['awayTeam']["score"], score2=item['homeTeam']["score"], homeTeam=item['homeTeam']['teamName']))
    return render(request, 'index.html', {
<<<<<<< HEAD
        'games':data})

def verPartidosAyer(request):

    ayer = datetime.now() - timedelta(days=1)
    ayer = ayer.strftime('%Y-%m-%d')

    scoreboard = scoreboardv2.ScoreboardV2(game_date=ayer)
=======
        'games':games})
    
def verPartidosManana(request):
    
    manana = datetime.now() - timedelta(days=1)
    manana = manana.strftime('%Y-%m-%d')

    scoreboard = scoreboardv2.ScoreboardV2(game_date=manana)
>>>>>>> leandro

    partidosDict = scoreboard.get_dict()

    recorte = partidosDict["resultSets"][1]["rowSet"]

    mapaPartidos = {}

    for partido in recorte:
        id_partido = partido[2]
        equipo = partido[5]+" "+partido[6]
        puntos = partido[22]
<<<<<<< HEAD
        logo = f'{equipo.replace(" ", "")}Logo.png'
=======
        print(partido)
>>>>>>> leandro

        # Si el ID del partido no existe, inicializamos con los datos actuales
        if id_partido not in mapaPartidos:
            mapaPartidos[id_partido] = {
                "equipo1": equipo,
                "puntos1": puntos,
<<<<<<< HEAD
                "equipo1Logo" : logo,
                "equipo2": None,
                "puntos2": None,
                "equipo2Logo" : None,
=======
                "equipo2": None,
                "puntos2": None,
>>>>>>> leandro
                "escudoEquipo2" : None,
            }
        else:
            # Si ya existe, completamos los datos faltantes
            if mapaPartidos[id_partido]["equipo2"] is None:
                mapaPartidos[id_partido]["equipo2"] = equipo
                mapaPartidos[id_partido]["puntos2"] = puntos
<<<<<<< HEAD
                mapaPartidos[id_partido]["equipo2Logo"] = logo
    
    return render(request,"ayer.html",{"mapaPartidos": mapaPartidos,"fecha":ayer})

=======

    return render(request,"manana.html",{"mapaPartidos": mapaPartidos,"fecha":manana})
    
                    
>>>>>>> leandro
