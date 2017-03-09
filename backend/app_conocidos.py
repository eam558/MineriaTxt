
#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import json
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

#reload(sys)
#print sys.getdefaultencoding()
#sys.setdefaultencoding('utf8')

"""
Para correr este script (montar el backend) hay que poner en la línea de comando: 

export FLASK_APP = app.py

y luego:

flask run

Si sale algo similar a 

* Serving Flask app "app"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Es porque todo salió bien y el backend está arriba. De lo contrario, hay errores serios en el código
"""

#Esta parte hay que dejarla igual SIEMPRE
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#Esto es un ejemplo de cómo se cargan los datos de un repositorio de datos 

pathapp = os.getcwd()
#print(pathapp)
pathapp = pathapp[0:len(pathapp) - 7]

with open(pathapp+'data/json/grafo_conocidos.json',encoding='utf8') as f:
	grafo_conocidos = json.load(f)

with open(pathapp+'data/json/frentes_grafo.json',encoding='utf8') as f: #frentes_grafo
	burbuja = json.load(f)	

with open(pathapp+'data/json/grafo_heatmap.json',encoding='utf8') as f:
	mapa = json.load(f)	

with open(pathapp+'data/json/grafo_actividades_nuevo.json',encoding='utf8') as f:
	importante = json.load(f)	

"""
Este es un ejemplo de un servicio web: este servicio devuelve 
los restaurantes que queden en una dirección que se recibe por medio 
de una request (probablemente el frontend tenía un campo de texto donde se coloca esa información).

La línea @app.route('/restaurantes') tiene el decorador @app.route(), que es para 
colocar la ruta que se usa para llamar este servicio (por ejemplo, http://localhost:9000/restaurantes retorna 
lo que retornaría esta función).

La función request.args.get() es para obtener el valor del parámetro 'direccion'
en la request que recibe este servicio por parte del frontend.

Finalmente se hace una consulta en el repositorio de datos y se retorna lo que se quiere...
"""

def quitar_tildes(word):
    return word.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

def aristas_salientes(iden):
	out = [arista for arista in grafo_conocidos['aristas'] if arista['source']==iden]
	return out

def dar_nodo(nombre,nombre_archivo):
	for nodo in grafo_conocidos['nodos']:
		if nodo["id"]==nombre :
			return nodo


def nodos_salientes(iden):
	aristas = aristas_salientes(iden)
	rta=[]
	for arista in aristas:
		for nodo in grafo_conocidos["nodos"]:
			if nodo["id"]==arista["target"]:
				rta.append(nodo)
	return rta

@app.route('/grafo_conocidos')
def get_conocidos():
	
	frente = request.args.get('frente')
	nombre = request.args.get('nombre')
	alias = request.args.get('alias')
	frentes_relacionados = []

	rta = {}
	if nombre != "" and alias == "":
		for frente_actual in grafo_conocidos.keys():
			nodos = []
			id_nodos=[]
			aristas = []
			incluir_nodos = False
			incluir_aristas = False
			for nodo in grafo_conocidos[frente_actual]["nodos"]:
				if nodo["nombre"] == nombre:
					incluir_nodos = True
					incluir_aristas = True
					frentes_relacionados.append(frente_actual)
					for nodo in grafo_conocidos[frente_actual]["nodos"]:
						if nodo["id"] not in id_nodos:
							id_nodos.append(nodo["id"])
							nodos.append(nodo)
			aristas += grafo_conocidos[frente_actual]["aristas"]
			if incluir_nodos and incluir_aristas:	
				rta[frente_actual] = {"nodos": nodos, "aristas": aristas}

	elif nombre == "" and alias != "":
		for frente_actual in grafo_conocidos.keys():
			nodos = []
			id_nodos=[]
			aristas = []
			incluir_nodos = False
			incluir_aristas = False
			for nodo in grafo_conocidos[frente_actual]["nodos"]:
				if nodo["nombre"] == alias:
					incluir_nodos = True
					incluir_aristas = True
					frentes_relacionados.append(frente_actual)
					for nodo in grafo_conocidos[frente_actual]["nodos"]:
						if nodo["id"] not in id_nodos:
							id_nodos.append(nodo["id"])
							nodos.append(nodo)
			aristas += grafo_conocidos[frente_actual]["aristas"]
			if incluir_nodos and incluir_aristas:	
				rta[frente_actual] = {"nodos": nodos, "aristas": aristas}

	frentes_relacionados = list(set(frentes_relacionados))
	return jsonify(frentes_relacionados = frentes_relacionados, respuesta = rta)

	"""
	if frente!='' and nombre=='' and alias =='':
		rta={}
		for frente_actual in grafo_conocidos.keys():
			if str(frente_actual)==frente:
				rta=grafo_conocidos[frente_actual]
		return json.dumps(rta)	
	if frente=="" and nombre!='' and alias=="":
		rta={}
		for frente_actual in grafo_conocidos.keys():
			for nodo in grafo_conocidos[frente_actual]["nodos"]:
				if nodo["nombre"]==nombre:
					rta[frente_actual]=grafo_conocidos[frente_actual]
		return json.dumps(rta)	
	if frente!='' and nombre!='' and alias=='':
		rta={}
		
		for nodo in grafo_conocidos[frente]["nodos"]:
			if nodo["nombre"]==nombre:
				rta=grafo_conocidos[frente]
		return json.dumps(rta)				
	"""				


@app.route('/actividades')
def get_actividades_frente():
	return json.dumps(burbuja)


@app.route('/mapa')
def get_mapa():
	actividad = request.args.get('actividad')
	if actividad=="":
		return json.dumps({"coordenadas":[]})
	for key in mapa.keys():
		if key==actividad:
			return json.dumps(mapa[key])

@app.route('/parrafo')
def get_parrafo():
	id_nodo = request.args.get('id')
	frente_nodo=request.args.get('frente')
	actividad = request.args.get('actividad')

	parrafos =[]
	for nodo in importante[frente_nodo][actividad]['nodos']:
		if nodo['id']==id_nodo:
			parrafos.append(nodo['contexto'])

	return jsonify(parrafos = parrafos)

@app.route('/frente_actividades')
def get_subgrafo():
	frente = request.args.get('frente')
	actividad = request.args.get('actividad')
	nodos = []
	id_nodos=[]
	aristas = []
	rta ={}

	for frente_actual in importante.keys():
		if frente_actual == frente:
			nodos.append({"id":frente,'frente':frente,"tipo_de_nodo":"frente",'contexto':''})
			id_nodos.append(frente)
			if actividad != '':
				for delito in importante[frente_actual].keys():
					if delito == actividad:
						rta = importante[frente_actual][delito]
						return json.dumps(rta)
			else:
				for delito in importante[frente_actual].keys():
					if delito != '' and delito != 'nodos' and delito != 'aristas':
						for nodo in importante[frente_actual][delito]["nodos"]:
							if nodo["id"] not in id_nodos:
								id_nodos.append(nodo["id"])
								nodos.append(nodo)
						aristas += importante[frente_actual][delito]["aristas"]

				rta["nodos"] = nodos
				rta["aristas"] = aristas
				return json.dumps(rta)


