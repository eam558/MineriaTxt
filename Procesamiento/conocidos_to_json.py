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

def tipo_miembro(nombre):
	for c in nombre:
		print c
	return nombre

#dicc={"nodos":[],"aristas":[]}

dicc={}
for ent in features["entrevistas"]:
	frente = ent["frente"]
	contenido={"nodos":[],"aristas":[]}
 #nivel 1
	frente = ent["frente"]
	nombre_archivo = ent["nombre_archivo"]
   #nodo frete
	if frente !="":
		contenido["nodos"].append({"nombre": frente, "tipo_nodo": "frente", "cargo": "", "id":frente ,
								   "nombre_archivo":nombre_archivo,"estructura":frente})
		#nodo entrevistado
		nombre = ent["nombre_entrevistado"]
		contenido["nodos"].append(
				{"nombre": nombre, "tipo_nodo": "entrevistado", "cargo": "MIEMBRO", "id": nombre_archivo,
				 "nombre_archivo": nombre_archivo, "estructura": frente})

		#nodo nombres_conocidos
		for conocido in ent["nombres_conocidos"]:
			nodo = {"id": conocido, "nombre": conocido, "tipo_nodo": "nombre_conocido", "cargo": "",
					"nombre_archivo": nombre_archivo, "estructura": frente}
			contenido["nodos"].append(nodo)
			contenido["aristas"].append({"source": frente, "target": nombre_archivo, "tipo_de_relación": "Pertenece al frente"})
			contenido["aristas"].append({"source": nombre_archivo, "target": conocido, "tipo_de_relación": "Conocido del frente"})
		#nodo alias_conocidos
		for alias in ent["alias_conocidos"]:

			nodo = {"id": alias, "nombre": alias, "tipo_nodo": "alias_conocido", "cargo": ent["alias_conocidos"][alias]["tipo"],
					"nombre_archivo": nombre_archivo, "estructura": frente}
			contenido["nodos"].append(nodo)
			contenido["aristas"].append({"source": frente, "nombre_archivo":nombre_archivo, "target": nombre_archivo,
										 "tipo_de_relación": "Pertenece al frente"})
			contenido["aristas"].append({"source": nombre_archivo, "nombre_archivo":nombre_archivo, "target": alias,
										 "tipo_de_relación": "Conocido del frente"})

		dicc[frente]=contenido

with open(pathapp + "data/json/grafo_conocidos.json", 'w') as json_file:
	json.dump(dicc, json_file, indent=4, ensure_ascii=False)


