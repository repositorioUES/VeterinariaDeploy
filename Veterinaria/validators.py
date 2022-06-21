from django.db import models
from .models import *

from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError

def solo_Letras(value):
	
	letras = " 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóú"

	for i in value:
		if i not in letras:
			raise ValidationError('Este dato no es válido, deben ser sólo letras')


def solo_Numeros(num):
	if isinstance(num, int): #Comprobamos si es int para pasarlo a str
		num = str(num)
	numeros = "0123456789-"

	for i in num:
		if i not in numeros:
			raise ValidationError('Solo se permiten números')

def validar_Fecha(f):

	hoy = datetime.now().date() #Definimos la fecha dehoy

	if f > hoy: # Si es una fecha MAYOR que HOY --> mala
		raise ValidationError('La fecha NO debe ser mayor que la de hoy')
	
	bottom = hoy - timedelta(days=36500)
	if f < bottom: # Si es una fecha MENOR que HACE 100 AÑOS (36500 DIAS)--> mala
		raise ValidationError('La fecha NO debe ser muy antigua')

def fecha_mayor(f):

	hoy = datetime.now().date() #Definimos la fecha dehoy

	if f < hoy: # Si es una fecha MENOR que HOY --> mala
		raise ValidationError('La fecha NO debe ser menor que la de hoy')

def formato_Dui(dui):
	dui = str(dui)
	numeros = "0123456789"

	if len(dui) == 10:
		for i in range(10):
			if i != 8:
				if dui[i] not in numeros:
					raise ValidationError('DUI no cumple el formato, debe ser ########-#')
			else:
				if dui[i] != "-":
					raise ValidationError('DUI no cumple el formato, debe ser ########-#')
	else:
		raise ValidationError('DUI no cumple el formato, debe ser ########-#')

def formato_Telefono(tel):
	tel = str(tel)
	numeros = "0123456789"

	if len(tel) == 9:
		for i in range(9):
			if i != 4:
				if tel[i] not in numeros:
					raise ValidationError('Teléfono NO cumple el formato, debe ser ####-####')
			else:
				if tel[i] != "-":
					raise ValidationError('Teléfono NO cumple el formato, debe ser ####-####')
	else:
		raise ValidationError('Teléfono NO cumple el formato, debe ser ####-####')

def formato_Hora(hora):
	hora = str(hora)
	hayError = 0 # Si hay error = 1, si no = 0

	if len(hora) == 5:
		if hora[0] not in "01":
			hayError = 1
		
		if hora[0] == "0":
			if hora[1] not in "0123456789":
				hayError = 1
		elif hora[0] == "1":
			if hora[1] not in "012":
				hayError = 1
		
		if hora[2] != ":":
				hayError = 1

		if hora[3] not in "012345":
			hayError = 1
			
		if hora[4] not in "0123456789":
			hayError = 1
	else:
		hayError = 1
	
	if hayError == 1:
		raise ValidationError('Horario NO cumple el formato, debe ser ##:##')