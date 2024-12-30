from django import forms

class ingresarNombreJugador(forms.Form):
    nombre = forms.CharField(label="nombre jugador", max_length=50)