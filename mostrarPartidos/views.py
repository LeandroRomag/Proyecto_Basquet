from django.shortcuts import render
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import scoreboardv2
from datetime import datetime, timedelta
from nba_api.stats.static import teams
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
        'games':games})
    
def verPartidosManana(request):
    
    manana = datetime.now() - timedelta(days=1)
    manana = manana.strftime('%Y-%m-%d')

    scoreboard = scoreboardv2.ScoreboardV2(game_date=manana)

    partidosDict = scoreboard.get_dict()

    recorte = partidosDict["resultSets"][1]["rowSet"]

    mapaPartidos = {}

    for partido in recorte:
        id_partido = partido[2]
        equipo = partido[5]+" "+partido[6]
        puntos = partido[22]
        print(partido)

        # Si el ID del partido no existe, inicializamos con los datos actuales
        if id_partido not in mapaPartidos:
            mapaPartidos[id_partido] = {
                "equipo1": equipo,
                "puntos1": puntos,
                "equipo2": None,
                "puntos2": None,
                "escudoEquipo2" : None,
            }
        else:
            # Si ya existe, completamos los datos faltantes
            if mapaPartidos[id_partido]["equipo2"] is None:
                mapaPartidos[id_partido]["equipo2"] = equipo
                mapaPartidos[id_partido]["puntos2"] = puntos

    return render(request,"manana.html",{"mapaPartidos": mapaPartidos,"fecha":manana})
    
                    