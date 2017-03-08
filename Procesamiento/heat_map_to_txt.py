#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera el archivo data/csv/geo_ciudades.txt a paortir de los archivos
data/json/coordenadas.json generado por el get_coordenadas.py
data/json/features_documentos_nuevo.json generado por el scrip  extraccion_features.py
"""
import json
import os
import sys


# ajusto el sistema a utf8
reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')

pathapp = os.getcwd()
#print(pathapp)
pathapp = pathapp[0:len(pathapp) - 13]

with open(pathapp + "data/json/coordenadas.json", 'r') as f:
	coords_ciudades = json.load(f)

with open(pathapp + "data/json/features_documentos_nuevo.json",'r') as f:
	features = json.load(f)


delitos = list(features["entrevistas"][0]["delitos"].keys())
finanzas = list(features["entrevistas"][0]["finanzas"].keys())



#departamentos = set([quitar_tildes(x["departamento"]).lower() for x in coords_ciudades["coordenadas"]])

#localizaciones = ciudades+departamentos

def quitar_tildes(word):
    return word.replace(u"á", "a").replace(u"é", "e").replace(u"í", "i").replace(u"ó", "o").replace(u"ú", "u")
   

def buscar_coordenadas(ciudad):
	for coord_ciudad in coords_ciudades["coordenadas"]:
		if quitar_tildes(coord_ciudad["ciudad"]).lower() == quitar_tildes(ciudad.strip()).lower():
			return coord_ciudad
	return False


ciudades = set([quitar_tildes(x['ciudad']).lower() for x in coords_ciudades['coordenadas']])

def extract_ciudad(words):
	respuesta = ""
	respuesta_tmp = ""
	got_city = False
	for word in words:
		if word[0].isupper():
			respuesta_tmp += word + " "
			if quitar_tildes(word).lower() in ciudades and not got_city:
				respuesta += word + " "
				got_city = True
			else: 
				if quitar_tildes(respuesta_tmp).lower() in ciudades:
					respuesta = respuesta_tmp
					got_city = True
		else:
			if got_city:
				return respuesta
	return respuesta

def ciudades_en_texto(texto):
	ans = []
	texto = texto.replace(",", " , ").replace(".", " . ").replace(u"¿", u" ¿ ").replace(u"?", " ? ").replace("(", " ( ").replace(")", " ) ")
	palabras = texto.split()
	for i in range(len(palabras)-2):
		words = palabras[i:i+3]
		if len(extract_ciudad(words))>0:
			ans.append(extract_ciudad(words))

	return list(set(ans))		


with open(pathapp + "data/csv/geo_ciudades.txt", 'a') as f:
	def get_ciudades_actividad(actividad, tipo_actividad):
		ciudades_actividad = []

		for entrevista in features['entrevistas']:

			for act in entrevista[tipo_actividad].keys():
				if act == actividad:
					parrafos = entrevista[tipo_actividad][act]
					
					for parrafo in parrafos:
						ciudades_actividad+=ciudades_en_texto(parrafo)

		return ciudades_actividad
	i = 0
	for finanza in finanzas:
		f.write(finanza)
		lugares = get_ciudades_actividad(finanza, "finanzas")
		if len(lugares) >0:
			for lugar in lugares:
				coord = buscar_coordenadas(lugar)
				if coord:
					f.write (coord["ciudad"]+";"+coord["departamento"]+";"+str(coord["latitud"])+";"+str(coord["longitud"]))

				f.write("//")
		i += 1
		if i in [10, 20, 30, 50]:
			print(i)


	for delito in delitos:
		f.write(delito)
		lugares = get_ciudades_actividad(delito, "delitos")
		if len(lugares) >0:
			for lugar in lugares:
				coord = buscar_coordenadas(lugar)
				if coord:
					f.write(coord["ciudad"]+";"+coord["departamento"]+";"+str(coord["latitud"])+";"+str(coord["longitud"]))

		f.write("//")
		i += 1
		if i in [10, 20, 30, 50]:
			print(i)






