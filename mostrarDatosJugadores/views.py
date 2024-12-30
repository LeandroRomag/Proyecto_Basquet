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

#FUNCIONALIDAD QUE MUESTRA EL JUGADOR LUEGO DE OBTENERLO DESDE EL FORMULARIO
def mostrarJugador(req,nombre_jugador):
    jugador = players.find_players_by_full_name(nombre_jugador)
    jugadorStats = playercareerstats.PlayerCareerStats(player_id=jugador[0]["id"])
    jugadorStatsDICT = jugadorStats.get_dict()
    jugadorRetorno = {
        "nombre" : jugador[0]["full_name"],
        "id" : jugador[0]["id"],
        "estadisticasTemporadaRegular": safe_get(jugadorStatsDICT, 0),
        "estadisticasPlayOff": safe_get(jugadorStatsDICT, 2)
    }
    return render(req,"datosJugador.html",{"datos" : jugadorRetorno})

#FUNCIONALIDAD POR SI EL JUGADOR NUNCA JUGO PLAY OFF, ANTES SE ROMPIA SI NUNCA JUGO PLAY OFF
def safe_get(stats_dict, result_set_index, row_index=-1):
    try:
        return stats_dict['resultSets'][result_set_index]['rowSet'][row_index]
    except (KeyError, IndexError):
        return None

#FUNCIONALIDAD QUE TRABAJA CON EL PROMPT ENVIADO DESDE FORM, LA FUNCIONALIDAD ESTA EN LA VIEW
def buscar_jugadores(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        jugadores = players.find_players_by_full_name(nombre)[:5]
        return JsonResponse({'jugadores': jugadores})
    return JsonResponse({'mensaje': 'No se proporcionó un nombre'})
