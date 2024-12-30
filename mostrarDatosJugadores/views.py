from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from .forms import ingresarNombreJugador

# Create your views here.
def recibidorDeEvento(req):
    if req.method == "GET":
        return render(req,"formJugador.html", {
            'form' : ingresarNombreJugador()
        })
    else:
        query = req.POST["nombre"]
        return redirect('/jugador/' + query)
    
def mostrarJugador(req,nombre_jugador):
    jugador = players.find_players_by_full_name(nombre_jugador)
    jugadorStats = playercareerstats.PlayerCareerStats(player_id=jugador[0]["id"])
    jugadorStatsDICT = jugadorStats.get_dict()
    jugadorRetorno = {
        "nombre" : jugador[0]["full_name"],
        "id" : jugador[0]["id"],
        "estadisticasTemporadaRegular" : jugadorStatsDICT['resultSets'][0]['rowSet'][len(jugadorStatsDICT['resultSets'][0]['rowSet'])-1],
        "estadisticasPlayOff" : jugadorStatsDICT['resultSets'][2]['rowSet'][len(jugadorStatsDICT['resultSets'][2]['rowSet'])-1]
    }
    return render(req,"datosJugador.html",{"datos" : jugadorRetorno})

def buscar_jugadores(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        jugadores = players.find_players_by_full_name(nombre)[:5]
        return JsonResponse({'jugadores': jugadores})
    return JsonResponse({'mensaje': 'No se proporcionó un nombre'})
