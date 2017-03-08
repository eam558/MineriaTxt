#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import sys
import os

# ajusto el sistema a utf8
reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')

pathapp = os.getcwd()
pathapp = pathapp[0:len(pathapp) - 13]

with open(  pathapp +   "data/json/features_documentos_nuevo.json",'r') as f:
	features = json.load(f)

def es_cabecilla(nombre):
	return nombre

#dicc={"nodos":[],"aristas":[]}

dicc={}
frentes=[x["frente"] for x in features["entrevistas"]]

print frentes

for frente in frentes:
	if frente !="":
	 	nodo=[ frente, frente]
		dicc[frente]=nodo



#print frente

"""	nodo={"id":frente, "nombre": frente,"tipo_nodo":"frente", "cabecilla": "NO"}
	dicc["nodos"].append(nodo)


	for ent in features["entrevistas"]:
		frente=ent["frente"]
	#print ent
		nombre=ent["nombre_entrevistado"]
		nombre_archivo=ent["nombre_archivo"]
		dicc["nodos"].append({"id":nombre_archivo,"nombre":nombre,"tipo_nodo":"entrevistado","cabecilla":es_cabecilla(nombre)})


for conocido in ent["nombres_conocidos"]:
    nodo={"id":conocido, "nombre":conocido,"tipo_nodo":"nombre_conocido", "cabecilla": es_cabecilla(conocido)}
    dicc["nodos"].append(nodo)
    dicc["aristas"].append({"source":frente, "target":nombre_archivo, "tipo_de_relación":"Pertenece al frente"})
    dicc["aristas"].append({"source":nombre_archivo,"target":conocido,"tipo_de_relación":"Conocido del frente"})
for alias in ent["alias_conocidos"]:
    nodo={"id":alias, "nombre":alias,"tipo_nodo":"alias_conocido", "cabecilla": es_cabecilla(alias)}
    dicc["nodos"].append(nodo)
    dicc["aristas"].append({"source":frente, "target":nombre_archivo, "tipo_de_relación":"Pertenece al frente"})
    dicc["aristas"].append({"source":nombre_archivo,"target":alias,"tipo_de_relación":"Conocido del frente"})
"""


with open(pathapp + "data/json/grafo_conocidos_1.json", 'w') as json_file:
	json.dump(dicc, json_file, indent=4, ensure_ascii=False)


