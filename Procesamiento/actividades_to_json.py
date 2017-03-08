#!/usr/bin/env python
# _*_ coding: latin-1 _*_

"""
a partir del archivo  features_documentos_nuevo.json (generado po extraccionfeatures.py) genera el archivo grafo_actividades_nuevo.json

"""

import re
import json
import os
import io
import sys


# ajusto el sistema a utf8
reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')

import pandas as pd
from collections import defaultdict

pathapp = os.getcwd()
#print(pathapp)
pathapp = pathapp[0:len(pathapp) - 13]

with io.open(pathapp + "data/json/features_documentos_nuevo.json",'r',encoding='utf-8') as f:
	features = json.load(f)
"""
with open("/home/abue/Documents/georref_actividades.json",'r') as f:
	actividades = json.load(f)
"""

def quitar_tildes(word):
    return word.replace(u"á", "a").replace(u"é", "e").replace(u"í", "i").replace(u"ó", "o").replace(u"ú", "u")

#todas las actividades a buscar
def get_todas_actividades():
	todas_act={}
	entrevista1=features['entrevistas'][0]
	for act in entrevista1['finanzas'].keys():
		todas_act[act]='finanzas'
	for act in entrevista1['delitos'].keys():
		todas_act[act]='delitos'
	return todas_act

#todos los keys de actividades existentes dado un frente
def get_actividades_frente(frente):
	actividades_frente=[]
	act_finanzas=[]
	act_delitos=[]
	for ent in get_entrevistas_frente(frente):
		for actividad in ent['finanzas'].keys():

			if len(ent['finanzas'][actividad])>0:
				act_finanzas.append(actividad)
		for actividad in ent['delitos'].keys():
			if len(ent['delitos'][actividad])>0:
				act_finanzas.append(actividad)	
	actvidades_frente=set(act_finanzas+act_delitos)
	return actvidades_frente
# return entrevistas dado un frente
def get_entrevistas_frente(frente):
	return [ent for ent in features['entrevistas'] if ent['frente']==frente]


#--------------------------------------------------------------------------
# CIUDADES
#--------------------------------------------------------------------------

with open(pathapp + "data/json/coordenadas.json", 'r') as f:
	coords_ciudades = json.load(f)

ciudades = set([quitar_tildes(x["ciudad"]).lower() for x in coords_ciudades["coordenadas"]])

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
	texto = texto.replace(",", " , ").replace(".", " . ").replace(u"¿", u" ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")
	palabras = texto.split()
	for i in range(len(palabras)-2):
		words = palabras[i:i+3]
		if len(extract_ciudad(words))>0:
			ans.append(extract_ciudad(words))
	ans=[x.strip() for x in list(set(ans))]
	return ans

def get_ciudad_actividad(actividad,tipo_act,frente):
	ciudades_act=[]
	for ent in get_entrevistas_frente(frente):
		parrafos=ent[tipo_act][actividad]
		for parrafo in parrafos:
			ciudades = ciudades_en_texto(parrafo)
			if len(parrafo)>0 and len(ciudades) > 0:
				ciudades_act+=[(ciudad, parrafo) for ciudad in ciudades]
	return ciudades_act

#--------------------------------------------------------------------------
# ALIAS
#--------------------------------------------------------------------------

def is_alias(words):
	sin_salto_linea = words.replace("//", "")
	alias_tipo_1 = re.search("[A|a]lias\s*[A-Z]", sin_salto_linea)
	alias_tipo_2 = re.search("\(\s*a\s*\.(.+?)\)", words)
	if alias_tipo_1 is not None or alias_tipo_2 is not None:
		return True
	else:
		return False

def has_cargo(array):
	for element in array:
		if 'cabecilla' in element.lower() or 'mando' in element.lower() or 'jefe' in element.lower():
			return True
	else: 
		return False

def has_estructura(array):
	i = 0
	digitos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	for element in array:
		if i >0 and i < len(array) - 1:
			rodeado_de_nombre = array[i+1][0].isupper() or array[i-1][0] in digitos or array[i+1][0] in digitos
			if ('frente' in element.lower() and rodeado_de_nombre) or 'columna' in element.lower() or 'cuadrilla' in element.lower() or (u'compañia' in element.lower() and rodeado_de_nombre):
				return True
		i += 1
	else: 
		return False

def extract_alias(array):
	alias_tipo_2 = re.search("\(\s*a\s*\.(.+?)\)", " ".join(array))
	if "alias" in array or "Alias" in array:
		alias = ""
		got_alias = False
		for element in array:
			if "alias" in element or "Alias" in element:
				if got_alias:
					break
				element = re.search("([a|A]lias.*)", element).group(1)
				alias += " " + element.replace("//", "")
				got_alias = True
			elif element[0].isupper() and got_alias:
				if re.findall("[A-Z]", element[1:]):
					alias += " " + re.search("(.+?)[A-Z]", element.replace("//", "")).group(1) 
				alias += " " + element.replace("//", "")
				got_alias = True
			else:
				if got_alias:
					break
		return alias
	elif alias_tipo_2 is not None:
		return "alias" + alias_tipo_2.group(1).replace("//", "").replace("( a .", "")
	else:
		return ""


def get_estructura(array):
	i = 0
	digitos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	for element in array:
		if i > 0 and i < len(array) - 1:
			if element.lower() == 'frente': 
				if array[i-1][0] in digitos:
					return "FRENTE "+array[i-1]
				elif array[i+1][0].isupper():
					nombre_estructura = ""
					got_nombre = False
					for word in array[i+1:]:
						if word[0].isupper() and 'alias' not in word.lower():
							nombre_estructura += word
							got_nombre = True
						else:
							if got_nombre:
								return "FRENTE "+ nombre_estructura.upper()
							if 'alias' in word:
								return "FRENTE "+nombre_estructura.upper()
				elif array[i+1][0] in digitos:
					return "FRENTE "+array[i+1]
				else:
					return "FRENTE"
			elif element.lower() == 'columna': 
				if array[i-1][0] in digitos:
					return "COLUMNA "+array[i-1]
				elif array[i+1][0].isupper():
					nombre_estructura = ""
					got_nombre = False
					for word in array[i+1:]:
						if word[0].isupper() and 'alias' not in word.lower():
							nombre_estructura += word
							got_nombre = True
						else:
							if got_nombre:
								return "COLUMNA "+ nombre_estructura.upper()
							if 'alias' in word:
								return "COLUMNA "+nombre_estructura.upper()
				elif array[i+1][0] in digitos:
					return "COLUMNA "+array[i+1]
				else:
					return "COLUMNA"
			elif element.lower() == 'cuadrilla': 
				if array[i-1][0] in digitos:
					return "CUADRILLA "+array[i-1]
				elif array[i+1][0].isupper():
					nombre_estructura = ""
					got_nombre = False
					for word in array[i+1:]:
						if word[0].isupper() and 'alias' not in word.lower():
							nombre_estructura += word
							got_nombre = True
						else:
							if got_nombre:
								return "CUADRILLA "+ nombre_estructura.upper()
							if 'alias' in word:
								return "CUADRILLA "+nombre_estructura.upper()
				elif array[i+1][0] in digitos:
					return "CUADRILLA "+array[i+1]
				else:
					return "CUADRILLA"
			elif element.lower() == u'compañia':
				if array[i-1][0] in digitos:
					return u"COMPAÑIA "+array[i-1]
				elif array[i+1][0].isupper():
					nombre_estructura = ""
					got_nombre = False
					for word in array[i+1:]:
						if word[0].isupper() and 'alias' not in word.lower():
							nombre_estructura += word
							got_nombre = True
						else:
							if got_nombre:
								return u"COMPAÑIA "+ nombre_estructura.upper()
							if 'alias' in word:
								return u"COMPAÑIA "+nombre_estructura.upper()
				elif array[i+1][0] in digitos:
					return u"COMPAÑIA "+array[i+1]
				else:
					return u"COMPAÑIA"
		i += 1
	return ""

def get_cargo(array):
	i = 0
	for element in array:
		if i > 0 and i < len(array) - 1:
			if 'cabecilla' in element.lower(): 
				if array[i-1] in ["primero", "segundo", "tercero", "cuarto", "quinto", "sexto"]:
					return "CABECILLA "+array[i-1].upper()
				elif array[i+1] in ["primero", "segundo", "tercero", "cuarto", "quinto", "sexto"]:
					return "CABECILLA "+array[i+1].upper()
				else:
					return "CABECILLA"
			elif 'mando' in element.lower(): 
				if array[i-1] in ["primero", "segundo", "tercero", "cuarto", "quinto", "sexto"]:
					return "MANDO "+array[i-1].upper()
				elif array[i+1] in ["primero", "segundo", "tercero", "cuarto", "quinto", "sexto"]:
					return "MANDO "+array[i+1].upper()
				else:
					return "MANDO"
			if 'jefe' in element.lower():
				if "finanzas" in [x.lower() for x in array]:
					return "JEFE FINANZAS"
				elif "politico" in [quitar_tildes(x.lower()) for x in array]:
					return "JEFE POLÍTICA"
				else:
					return "JEFE"
		i += 1
	return ""

def get_alias_conocidos(text):
	ans = []
	text = text.replace("\n", " // ").replace(",", " , ").replace(".", " . ").replace(u"¿", u" ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")
	words = text.split()
	got_something = False
	done = False
	info = ""
	info_tmp = ""
	for i in range(len(words)-9):
		word = words[i:i+10]
		if is_alias(" ".join(word)) and len(extract_alias(word).split()) > 1:
			alias = extract_alias(word).strip()
			cargo = ""
			estructura = ""
			if has_cargo(word) and has_estructura(word):
				cargo = get_cargo(word).strip()
				estructura = get_estructura(word).strip()
	
				if len(estructura.split()) >1:
					info = (alias, cargo, estructura)
					#info = {"alias": alias, "cargo": cargo, "estructura": estructura}
				else:
					info = (alias, cargo, "")
					#info = {"alias": alias, "cargo": cargo, "estructura": ""}
				done = True
			else:
				if has_cargo(word):
					cargo = get_cargo(word).strip()
					info_tmp = (alias, cargo, "")
					#info_tmp = {"alias": alias, "cargo": cargo, "estructura": ""}
				elif has_estructura(word) and len(get_estructura(word).strip().split()) >1:
					estructura = get_estructura(word).strip()
					info_tmp = (alias, "MIEMBRO", estructura)
					#info_tmp = {"alias": alias, "cargo": "MIEMBRO", "estructura": estructura}
				else:
					info_tmp = (alias, "MIEMBRO", "")
					#info_tmp = {"alias": alias, "cargo": "MIEMBRO", "estructura": ""}
			got_something = True
			if i == len(words)-10:
				info = info_tmp
				ans.append(info)
		else:
			if got_something and not done:
				info = info_tmp
				info_tmp = ""
				done = True
		if done or i == len(words)-10:
			ans.append(info)
			got_something = False
			done = False
	ans=list(set(ans))
	return ans
		

def get_alias_actividad(actividad,tipo_act,frente):
	alias_act=[]
	for ent in get_entrevistas_frente(frente):
		parrafos=ent[tipo_act][actividad]
		for parrafo in parrafos:
			alias = get_alias_conocidos(parrafo)
			if len(parrafo)>0 and len(alias) > 0:
				alias_act+=[(nom[0],parrafo) for nom in alias if nom!=""]
	return alias_act


#--------------------------------------------------------------------------
# NOMBRES
#--------------------------------------------------------------------------


with open(pathapp + "data/json/diccionario_nombres.json", 'r') as f:
	dicc_nombres = json.load(f)

pronombres=['adonde', 'adónde', 'algo', 'alguien', 'alguna', 'algunas', 'alguno', 'algunos', 'ambas', 'ambos', 'aquel', 'aquél', 'aquella', 'aquélla', 'aquellas', 'aquéllas', 'aquello', 'aquellos', 'aquéllos', 'bastante', 'bastantes', 'como', 'cómo', 'conmigo', 'consigo', 'contigo', 'cual', 'cual', 'cuál', 'cuales', 'cuáles', 'cualesquiera', 'cualquiera', 'cuando', 'cuándo', 'cuanta', 'cuánta', 'cuantas', 'cuántas', 'cuanto', 'cuánto', 'cuantos', 'cuántos', 'cuya', 'cuyas', 'cuyo', 'cuyos', 'demás', 'demasiada', 'demasiadas', 'demasiado', 'demasiados', 'donde', 'dónde', 'él', 'ella', 'ellas', 'ello', 'ellos', 'esa', 'ésa', 'esas', 'ésas', 'ese', 'ése', 'eso', 'esos', 'ésos', 'esta', 'ésta', 'estas', 'éstas', 'este', 'éste', 'esto', 'estos', 'éstos', 'estotra', 'estotro', 'idem', 'ídem', 'la', 'las', 'le', 'les', 'lo', 'lo', 'los', 'me', 'media', 'medias', 'medio', 'medios', 'mí', 'misma', 'mismas', 'mismo', 'mismos', 'mucha', 'muchas', 'mucho', 'muchos', 'nada', 'nadie', 'ninguna', 'ningunas', 'ninguno', 'ningunos', 'nos', 'nosotras', 'nosotros', 'os', 'otra', 'otras', 'otro', 'otros', 'poca', 'pocas', 'poco', 'pocos', 'qué', 'que', 'qué', 'quien', 'quién', 'quienes', 'quiénes', 'quienesquiera', 'quienquier', 'quienquiera', 'se', 'sí', 'tal', 'tales', 'tanta', 'tantas', 'tanto', 'tantos', 'te', 'ti', 'toda', 'todas', 'todo', 'todos', 'tú', 'una', 'unas', 'uno', 'unos', 'usted', 'ustedes', 'varias', 'varios', 'vos', 'vosotras', 'vosotros', 'yo']
preposiciones=["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde","en", "entre", "hacia", "hasta", "para", "por", "según","segun", "sin","so", "sobre", "tras", "durante", "mediante", "versus" ,"via"]
articulos=["la, el, lo, su , a , sobre, de, los, las, suyo, su, sus, este, aquél, ese, mi, tu, nuestro, vuestro"]
conjunciones=['a', 'condición', 'de', 'que', 'a', 'menos', 'que', 'a', 'pesar', 'de', 'todo', 'a', 'pesar', 'de', 'además', 'de', 'además', 'adonde', 'adonde', 'quiera', 'que', 'ahora', 'que', 'antes', 'que', 'aún', 'así', 'aún', 'cuando', 'aunque', 'como', 'si', 'como', '(causa)', 'como', '(modo)', 'con', 'tal', 'que', 'cualquiera', 'que', 'sea', 'cuando', '(simultaneidad)', 'cuando', 'de', 'lo', 'contrario', 'desde', 'que', 'después', 'que', 'donde', 'donde', 'quiera', 'que', 'en', 'cuanto', 'hasta', 'que', 'lo', 'mismo', 'que', 'mientras', 'mientras', 'que', 'no', 'obstante', 'o', 'para', 'para', 'que', 'pero', 'por', 'por', 'miedo', 'a', 'por', 'mucho', 'que', 'por', 'muy', 'por', 'si', 'porque', 'puesto', 'que', 'si', 'siempre', 'que', 'sin', 'embargo', 'suponiendo', 'que', 'tan', 'pronto', 'como', 'una', 'vez', 'que', 'y', 'ya', 'que']

stopwords = pronombres + conjunciones + articulos + preposiciones
palabras_prohibidas = ["puerto", "san", "santa", "rojo", "rojos", "azul", "azules", "amarillo", "amarillos", "verde", "verdes", "blancos", "blancas", "negros", "negras", "orden", "día", "dia", "mes", "año", "semana", "nuevo", "viejo", "juzgado", "principal", "cara", "barba", "arco", "llama", "grado", "cola", "derecho", "izquierdo", "urbano", "rural", "pequeño", "grande", "seguro", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "corta", "corto", "largo", "larga", "cai", "bajo", "medio", "alto", "botas", "canta", "cuello", "orjeas", "pie", "pierna", "brazo", "boca", "pelo", "cabello", "raso", "batalla", "combate", "modelo", "fama", "hombre", "mujer", "niña", "niños", "niñas", "canto", "palo"]

columnas = ["YESID ORTIZ","TEOFILO FORERO","RUIZ BARI","REINEL MENDEZ","MILLER PERDOMO","MARISCAL SUCRE","MARIO VELEZ","LUIS PARDO","LIBARDO GARCÍA","JUAN JOSE RONDON","JACOBO PRIAS ALAPE","JACOBO ARENAS","GABRIEL GALVIS","DANIEL ALDANA","ARTURO RUIZ","ALIRIO TORRES","ALFONSO CASTELLANOS","VLADIMIR ESTIVEN","HEROES DE MARQUETALIA"]
frentes = ["COMBATIENTES DEL YARI","ACACIO MEDINA","VICTOR ALIRIO SAAVEDRA","VLADIMIR ESTIVEN","AMAZONICO","URIAS RONDON","URIAS CUELLAR","TULIO VARON","CACIQUE TIMANCO","REINALDO CUELLAR","POLICARPA SALABARRIETA","MARIO VELEZ","MANUELA BELTRAN","MANUEL CEPEDA VARGAS","JOSELO LOSADA","FELIPE RINCON","ESTEBAN RAMIREZ","DOMINGO BIOJO","CAMILO TABACO","AURELIO RODRIGUEZ","ANTONIO NARIÑO","ABELARDO ROMERO"]
estructuras = columnas + frentes


def has_stopword(words):
	lista_words = [x.lower() for x in words.split()]
	for word in lista_words:
		if quitar_tildes(word) in stopwords:
			return True
	else: 
		return False

def is_name(word):
	word_modificada_upper = quitar_tildes(word).upper()
	word_modificada_lower = quitar_tildes(word).lower()
	if (word[0].isupper() and (word_modificada_upper in dicc_nombres["nombres"] or word_modificada_upper in dicc_nombres["apellidos"])) and word_modificada_lower not in stopwords and word_modificada_lower not in palabras_prohibidas:
		return True
	else:
		return False

def is_place(array):
	for element in array:
		if quitar_tildes(element.lower()) in ["area", "areas", "vereda", "veredas", "finca", "fincas", "corregimiento", "corregimientos", "ciudad", "ciudades", "pueblo", "pueblos", "municipio", "municipios", "departamento", "departamentos", "ubicada", "ubicadas", "ubicado", "ubicados", "puente", "casa", "campo", "puerto", "puertos", "valle", "valles", "rio", "barrio", "comuna", "comunidad", "caño", "carrera", "via", "mar", "lago", "laguna", "norte", "sur", "este", "oeste", "occidente", "oriente", "cerro", "serrania", "monte", "selva", "llano"]:
			return True
	return False

def is_alias_nombre(words):
	lista_words = [x.lower() for x in words.split()]
	if "alias" in lista_words:
		return True
	else:
		return False

def extract_name(array):
	nombre = ""
	got_name = False
	for element in array:
		if is_name(element):
			nombre += " " + element
			got_name = True
		else:
			if got_name:
				break

	return nombre

def get_nombres(text):
	ans = []
	text = text.replace("\n", " ").replace(",", " , ").replace(".", " . ").replace(u"¿", u" ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")
	words = text.split()
	nombre_actual = ""
	max_name_length = 0
	got_name = False
	got_place = False
	for i in range(len(words)-3):
		word = words[i:i+4]
		if is_place(word):
			got_place = True
		elif sum([is_name(x) for x in extract_name(word).split()]) > 1:
			if not got_place and sum([is_name(x) for x in extract_name(word).split()]) > max_name_length:
				nombre_actual = extract_name(word)
				max_name_length = sum([is_name(x) for x in extract_name(word).split()])
			if i == len(words) - 4:
				ans.append(quitar_tildes(nombre_actual).strip())
			got_name = True
		else:
			got_name = False
			got_place = False
			max_name_length = 0
			if len(nombre_actual.strip()) > 0 and not is_alias_nombre(nombre_actual.strip()) and not quitar_tildes(nombre_actual.strip()).upper() in estructuras and not has_stopword(nombre_actual.strip()):
				ans.append(quitar_tildes(nombre_actual).strip())
				nombre_actual = ""
	ans=[x.strip() for x in list(set(ans))]
	return ans

#dada una actividad y su tipo (finanzas, delitos) y el frente, devuelve los nombres
def get_nombres_actividad(actividad,tipo_act,frente):
	nombres_act=[]
	for ent in get_entrevistas_frente(frente):
		parrafos=ent[tipo_act][actividad]
		for parrafo in parrafos:
			nombres = get_nombres(parrafo)
			if len(parrafo)>0 and len(nombres) > 0:
				nombres_act+=[(nombre, parrafo) for nombre in nombres]
	return nombres_act

#--------------------------------------------------------------------------
# MONTOS
#--------------------------------------------------------------------------

def montos_texto(texto):
	texto=texto.replace("\n"," ")
	try:
		return re.findall('[A-z0-9]+\smillones|[0-9\.]+0{3}|[A-z0-9]+\skilos|[A-z0-9]+\shectáreas|[A-z0-9]+\smillones|[A-z0-9]+\stoneladas',texto)
	except:
		return []

def get_montos_actividad(actividad,tipo_act,frente):
	montos_act=[]
	for ent in get_entrevistas_frente(frente):
		parrafos=ent[tipo_act][actividad]
		for parrafo in parrafos:
			montos = montos_texto(parrafo)
			if len(parrafo)>0 and len(montos) > 0:
				montos_act+=[(monto, parrafo) for monto in montos]
	return montos_act


##########################################################################
#Construcción del grafo
##########################################################################

def grafo_frente(frente):
	dicc={}
	dicc['nodos']=[]
	dicc['aristas']=[]

	nodo={"id":frente,'frente':frente,"tipo_de_nodo":"frente",'contexto':''}


	for actividad in get_actividades_frente(frente):

		dicc[actividad]={}
		dicc[actividad]['nodos']=[]
		dicc[actividad]['aristas']=[]
		#dicc[actividad]['nodos'].append(nodo)


		total_actividades = get_todas_actividades()
		tipo_actividad=total_actividades[actividad]#deito o finanzas
		dicc[actividad]['nodos'].append({'id':actividad,'frente':frente,'tipo_de_nodo':'actividad','contexto':'','actividad':actividad})
		dicc[actividad]['aristas'].append({'source':frente,'target':actividad})#arista del frente a actividad
#		
		dicc[actividad]['nodos'].append({'id':'nombres'+' '+actividad,'frente':frente,'tipo_de_nodo':'característica','contexto':'','actividad':actividad})
		dicc[actividad]['aristas'].append({'source':actividad,'target':'nombres'+" "+actividad})
		for nombre,parrafo in get_nombres_actividad(actividad,tipo_actividad,frente):
			dicc[actividad]['nodos'].append({'id':nombre,'frente':frente,'tipo_de_nodo':'nombre','contexto':parrafo,'actividad':actividad})
			dicc[actividad]['aristas'].append({'source':'nombres'+" "+actividad,'target':nombre})
#
		dicc[actividad]['nodos'].append({'id':'alias'+' '+actividad,'frente':frente,'tipo_de_nodo':'característica','contexto':'','actividad':actividad})
		dicc[actividad]['aristas'].append({'source':actividad,'target':'alias'+" "+actividad})		
		for alias,parrafo in get_alias_actividad(actividad,tipo_actividad,frente):
			dicc[actividad]['nodos'].append({'id':alias,"frente":frente,'tipo_de_nodo':'alias','contexto':parrafo,'actividad':actividad})
			dicc[actividad]['aristas'].append({'source':'alias'+" "+actividad,'target':alias})
#
		dicc[actividad]['nodos'].append({'id':'ciudad'+' '+actividad,'frente':frente,'tipo_de_nodo':'característica','contexto':'','actividad':actividad})
		dicc[actividad]['aristas'].append({'source':actividad,'target':'ciudad'+" "+actividad})		
		for ciudad,parrafo in get_ciudad_actividad(actividad,tipo_actividad,frente):
			dicc[actividad]['nodos'].append({'id':ciudad,"frente":frente,'tipo_de_nodo':'ciudad','contexto':parrafo,'actividad':actividad})
			dicc[actividad]['aristas'].append({'source':'ciudad'+" "+actividad,'target':ciudad})
#
		dicc[actividad]['nodos'].append({'id':'montos'+' '+actividad,'frente':frente,'tipo_de_nodo':'característica','contexto':'','actividad':actividad})
		dicc[actividad]['aristas'].append({'source':actividad,'target':'montos'+" "+actividad})		
		for monto,parrafo in get_montos_actividad(actividad,tipo_actividad,frente):
			dicc[actividad]['nodos'].append({'id':monto,"frente":frente,'tipo_de_nodo':'monto','contexto':parrafo,'actividad':actividad})
			dicc[actividad]['aristas'].append({'source':'montos'+" "+actividad,'target':monto})		



	return dicc


dicc_total={}

frentes=list(set([x['frente'] for x in features['entrevistas'] if len(x['frente'].strip())>0]))

for frente in frentes:
	dicc_total[frente]=grafo_frente(frente)
	print(frente)

#print dicc_total
with open( pathapp + 'data/json/grafo_actividades_nuevo.json', 'w') as json_file:
    json.dump( dicc_total, json_file, indent=4,ensure_ascii=False)
