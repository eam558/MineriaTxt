#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import re
import json

with open("/home/otaivin/Trabajo/MineriaTxt/Preprocesamiento_II/extraccion_features/diccionario_nombres.json", 'r') as f:
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

def quitar_tildes(word):
    return word.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

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

def is_alias(words):
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
	text = text.replace("\n", " ").replace(",", " , ").replace(".", " . ").replace("¿", " ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")
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
			if len(nombre_actual.strip()) > 0 and not is_alias(nombre_actual.strip()) and not quitar_tildes(nombre_actual.strip()).upper() in estructuras and not has_stopword(nombre_actual.strip()):
				ans.append(quitar_tildes(nombre_actual).strip())
				nombre_actual = ""
	return ans

"""
with open("/home/abue/Documents/nombres.txt", 'r') as f:
	archivos = [x.strip() for x in f.read().split('\n') if len(x.strip())>0]

i = 0
with open("conocidos.txt", 'a') as fwrite:
	for archivo in archivos:
		print(archivo, file=fwrite)
		with open("/home/abue/Documents/datos_limpios/"+archivo, 'r') as f:
			texto = f.read()
			for nombre in set(get_nombres(texto)):
				print(nombre, file=fwrite)
			print("//", file=fwrite)
		i += 1
		if i in [100, 300, 500, 700]:
			print("Van "+str(i))

"""

print(get_nombres('mi nombre es Cesar Méndez y trabajo con David Jaramillo'))
