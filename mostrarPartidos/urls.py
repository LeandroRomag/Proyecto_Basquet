from django.urls import path
from . import views
urlpatterns=[
    path ('', views.verPartidos),
    path ('ayer/', views.verPartidosAyer),
    path ('manana/', views.verPartidosManana)
]