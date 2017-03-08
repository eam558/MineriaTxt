#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera el archivo grafo_heatmap.json a partir del archivo /data/csv/geo_ciudades.txt'
"""
from collections import Counter
import json
import os

pathapp = os.getcwd()
#print(pathapp)
pathapp = pathapp[0:len(pathapp) - 13]

with open(pathapp +'/data/csv/geo_ciudades.txt') as f:
	texto_nombres = f.read()

bloques_delitos = texto_nombres.split('//')


ciudades = []
dicc_delitos={}
for bloque in bloques_delitos:
	lineas = [lin for lin in bloque.split('\n') if len(lin.strip())>0]
	delito = lineas[0]
	del lineas[0]
	dicc_delitos[delito]={}
	dicc_delitos[delito]['coordenadas']=[]

	ciudades_total=[]
	for linea in lineas:
		palabras =linea.split(';')
		tupla=(palabras[0],palabras[1],palabras[2],palabras[3])
		
		ciudades_total.append(tupla)
	contador=Counter(ciudades_total)

	for key in contador.keys():
		dicc_delitos[delito]['coordenadas'].append([float(key[2]),float(key[3]),contador[key]])


#print(dicc_delitos)


with open(pathapp + 'data/json/grafo_heatmap.json', 'w') as json_file:
    json.dump(dicc_delitos, json_file, indent=4, ensure_ascii=False)

"""

secuestro
bogota;cundinamarca;4444;54564574
barrancabermeja;Santander;34536;45654
bogota;cundinamarca;4444;54564574
bogota;cundinamarca;4444;54564574
bogota;cundinamarca;4444;54564574
"""