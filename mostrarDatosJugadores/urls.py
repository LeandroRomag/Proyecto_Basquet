from django.urls import path
from . import views
urlpatterns=[
    path('',views.recibidorDeEvento),
    path('/<str:nombre_jugador>/', views.mostrarJugador),
    path('/buscar_jugadores/datos', views.buscar_jugadores)
]