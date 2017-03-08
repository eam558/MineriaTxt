#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
Crea el archivo de coordenadas coordenadas.joson de los mincipios de colombia

"""
import re
import json
import os

pathapp = os.getcwd()
#print(pathapp)
pathapp = pathapp[0:len(pathapp) - 13]

def convertir_coordenada(coordenada):
	componentes = coordenada.split(";")
	grados = float(componentes[0].replace("&deg", ""))
	minutos = float(componentes[1].replace("&prime", ""))
	segundos = float(componentes[2].replace("&Prime", ""))
	if componentes[3] == 'W' or componentes[3] == 'S':
		return (grados + (segundos/3600) + (minutos/60))*-1
	else:
		return grados + (segundos/3600) + (minutos/60)

def limpiar_tags(text):
	sin_tags = re.sub("<[^<]+?>", "", text)
	texto_limpio = sin_tags.replace("&ntilde;", "ñ").replace("&aacute;", "á").replace("&eacute;", "é").replace("&iacute;", "í").replace("&oacute;", "ó").replace("&uacute;", "ú")
	return texto_limpio

def get_info(row):
	campos = re.findall("<td[^<]*?>.+?</td>", row)
	out = {
		"ciudad": limpiar_tags(campos[0]),
		"latitud": convertir_coordenada(limpiar_tags(campos[1])),
		"longitud": convertir_coordenada(limpiar_tags(campos[2])),
		"departamento": limpiar_tags(campos[4])
	}
	return out
	return out

out = {}
coordenadas = []

for i in range(1, 583):
	with open(pathapp + "data/coordenadas/Colombia-"+str(i)+".html", 'r') as f:
		text = f.read()

	tabla = text.split("<table class='table data'>")[1]
	filas = re.findall("<tr>.+?</tr>", tabla)
	coordenadas += [get_info(fila) for fila in filas if len(re.findall("<td[^<]*?>.+?</td>", fila)) > 0]

out["coordenadas"] = coordenadas


with open(pathapp+ 'data/json/coordenadas.json', 'w') as json_file:
    json.dump(out, json_file, indent=4, ensure_ascii=False)
