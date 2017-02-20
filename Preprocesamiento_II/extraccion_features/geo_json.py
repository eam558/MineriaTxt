import json
import pandas as pd
from collections import defaultdict

with open("/home/carlos/Documents/coordenadas.json", 'r') as f:
	coords_ciudades = json.load(f)

with open("/home/carlos/Documents/features_documentos.json",'r') as f:
	features = json.load(f)


delitos = list(features["entrevistas"][0]["delitos"].keys())
finanzas = list(features["entrevistas"][0]["finanzas"].keys())

def quitar_tildes(word):
    return word.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

def buscar_coordenadas(ciudad):
	for coord_ciudad in coords_ciudades["coordenadas"]:
		if quitar_tildes(coord_ciudad["ciudad"]).lower() == quitar_tildes(ciudad).lower():
			return coord_ciudad
	return False				

def buscar_ciudad(ciudad):
	for coord_ciudad in coords_ciudades["coordenadas"]:
		if quitar_tildes(coord_ciudad["ciudad"]).lower() == quitar_tildes(ciudad).lower():
			return True
	return False

def extract_ciudad(words):
	respuesta = ""
	respuesta_tmp = ""
	got_city = False
	for word in words:
		if word[0].isupper():
			respuesta_tmp += word + " "
			if buscar_ciudad(word) and not got_city:
				respuesta += word + " "
				got_city = True
			else: 
				if buscar_ciudad(respuesta_tmp):
					respuesta = respuesta_tmp
					got_city = True
		else:
			if got_city:
				return respuesta
	return respuesta

def contar_apariciones(array):
	out = defaultdict(int)
	for element in array:
		out[element] += 1
	return dict(out)

def ciudades_en_texto(texto):
	ans = []
	texto = texto.replace(",", " , ").replace(".", " . ").replace("¿", " ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")	
	palabras = texto.split()
	for i in range(len(palabras)-2):
		words = palabras[i:i+3]
		if len(extract_ciudad(words))>0:
			ans.append(extract_ciudad(words))

	return ans				

def get_ciudades_actividad(actividad, str_categoria):
	ciudades_actividad = []
	ciudades_actividad_tmp = []
	for entrevista in features["entrevistas"]:
		parrafos = entrevista[str_categoria][actividad]
		for parrafo in parrafos:
			ciudades_actividad_tmp += ciudades_en_texto(parrafo)
	for ciudad, conteo in contar_apariciones(ciudades_actividad_tmp).items():
		if buscar_coordenadas(ciudad):
			info = {
				"ciudad": buscar_coordenadas(ciudad)["ciudad"],
				"departamento": buscar_coordenadas(ciudad)["departamento"],
				"latitud": buscar_coordenadas(ciudad)["latitud"],
				"longitud": buscar_coordenadas(ciudad)["longitud"],
				"conteo": conteo
			}
			ciudades_actividad.append(info)
	return ciudades_actividad


def georr_actividades():
	out = {"actividades": {}}
	for delito in delitos:
		out["actividades"][delito] = get_ciudades_actividad(delito, "delitos")
	for finanza in finanzas:
		out["actividades"][finanza] = get_ciudades_actividad(finanza, "finanzas")
	return out
"""
with open('georr_actividades.json', 'w', encoding='utf8') as json_file:
    json.dump(georr_actividades(), json_file, indent=4, ensure_ascii=False)
"""

"""
with open("/home/carlos/Documents/datos_limpios/0688-03_Entrevista_militar.txt",'r') as f:
	print(ciudades_en_texto(f.read()))
"""
print(ciudades_en_texto("Hola yo soy de Medellín (Antioquia), Manizales, Barrancas y Santa Marta"))