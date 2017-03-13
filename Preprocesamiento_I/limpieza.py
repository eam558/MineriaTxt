#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import pdb
import os
import sys
import argparse
import datetime

# ajusto el sistema a utf8
reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('latin-1')

one_word_conjunction = ['y', 'a', 'e', 'o', 'u']
char_end_allowed = ['a', 'e', 'o', 'u', 'n', 'r', 's', 'l']

def pegar_tripletas(w1, w2, w3):
	separados = w1 + " " + w2 + " " + w3

	if len(w1) > 1:
		if len(w2) > 1: return separados

		else:
			if w2 in one_word_conjunction: 
				if w2 == 'e' or w2 == 'u':
					if (w2 == 'e' and w3[0].lower() == 'i') or (w2 == 'u' and w3[0].lower() == 'o'):
						return separados
					else:
						return w1 + " " + w2 + w3

				else:
					return separados

			else:
				return w1 + " " + w2 + w3

	else:
		if len(w3) > 1:
			if len(w2) > 1:
				if w1 in one_word_conjunction: 
					return separados
				else:
					return w1 + w2 + " " + w3

			else:
				if w1 == 'y':
					if w2 == 'a': return separados
					else:
						return w1 + " " + w2 + w3
				elif w2 not in char_end_allowed:
					return w1 + w2 + w3
				else:
					if w1 in ['a', 'e', 'o', 'u']:
						return w1 + w2 + " " + w3
					else: 
						return w1 + w2 + " " + w3

		else:
			if len(w2) > 1:
				if w1 in one_word_conjunction: return separados
				else:
					return w1 + w2 + " " + w3
			else:
				return w1 + w2 + w3

def limpiar_porcentajes(x):
	return x.group(0)[:-1]

def elimina_raros(texto):
	texto_limpio = re.sub(u'[^\xf1\xe1\xe9\xed\xf3\xfa\w\,\.\-\s\%\¿\?\(\)]', '', texto)
	texto_limpio = re.sub('[^0-9\s]\s*%', limpiar_porcentajes, texto_limpio)
	return texto_limpio

def separar(x):
	return x.group(0) + " "

def quitar_espacios(text):
	words = text.split()
	new_text = ""

	if len(words) < 3:
		return text

	for i in range(len(words)-2):
		w1 = words[i]
		w2 = words[i+1]
		w3 = words[i+2]

		if i != 0:
			if w3 not in pegar_tripletas(w1, w2, w3).split():
				new_text += w3
			else:
				new_text += " " + w3
		else:
			new_text += pegar_tripletas(w1, w2, w3)

	new_text = re.sub('([0-9]+|%)', separar, new_text)

	return new_text

#Elimina las mayusculas de una palabra
def separa_mayus(palabra):
	try:
		string_error = re.search('[a-zñ][A-Z]', palabra).group(0)
		fixed_string = string_error[0] + " " + string_error[1]
		return palabra.replace(string_error, fixed_string)
	except:
		return palabra		

#Elimina las mayusculas intermedias en todo el texto
def elimina_mayus(texto):
	todas = texto.split()
	todas_limpias = list(map(lambda x: separa_mayus(x), todas))
	return " ".join(todas_limpias)


def elimina_letras_sueltas(texto):
	words = texto.split()
	texto_limpio = ""

	for word in words:
		if len(word) ==1 and re.search('[a-zñ]', word) is not None and word not in one_word_conjunction:
			texto_limpio += ""
		else:
			texto_limpio += word + " "

	return texto_limpio


def known(words):
	"""
		Descarta si P(C)=0
	"""
	return set(w for w in words if w in NWORDS)

def known_edits2(word):
	"""
		Calcula el P(W/C) ----- distancia=2 y se descarta si P(C)=0
	"""
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

alphabet = u'abcdefghijklmnopqrstuvwxyz\xf1\xe1\xe9\xed\xf3\xfa'
def edits1(word): 
	"""
	Calcula el P(W/C) ----- distancia=1
	"""
	s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
	deletes= [a + b[1:] for a, b in s if b]
	transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]
	replaces= [a + c + b[1:] for a, b in s for c in alphabet if b]
	inserts= [a + c + b for a, b in s for c in alphabet]
	return set(deletes + transposes + replaces + inserts)


def correct(word):
	"""
	funcion principal
	"""
	if len(re.findall("[^0-9\,\.\-\s\%\¿\?\(\)]", word)) == 0:
		return word
	else:
		first_letter = ""
		candidates = known([word.lower()]) or known(edits1(word.lower())) or known_edits2(word.lower()) or [word.lower()]  
		candidato = max(candidates, key = NWORDS.get)
		if word[0].isupper():
			answer = word[0] + candidato[1:]
			return answer
		else:
			return candidato

def limpiar_linea(sentence):
	linea = sentence.replace(",", " , ").replace(".", " . ").replace("¿", " ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")	
	linea_limpia = elimina_letras_sueltas(elimina_mayus(quitar_espacios(elimina_raros(linea))))
	linea_corregida = " ".join([correct(x) for x in linea_limpia.split()])
	linea_corregida = linea_corregida.replace(" , ", ",").replace(" . ", ".").replace(" ? ", "?").replace(" ( ", "(").replace(" ) ", ")")
	return linea_corregida

pathapp = os.getcwd()
pathapp = pathapp[0:len(pathapp) - 18]




parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
args = parser.parse_args()

archivo = args.file

conteo=0
print pathapp
#abre el archivo de corpus 
with open(pathapp + "data/json/corpus.json", 'r') as f:
	NWORDS = json.load(f)

with open( pathapp+ "data/" + archivo , 'r') as f:
	lines = f.readlines()
	print datetime.datetime.now()
	for line in lines:
		conteo +=1

		line=line.rstrip('\n')
		line = line.rstrip('\r')
		with open( pathapp + "data/txt/" +line, 'r') as fread:
			try:
				#lineas_texto = [x.strip() for x in fread.readlines() if len(x.strip()) > 0]
				lineas_texto=[]
				for x in fread.readlines():
					linea = x.strip()
					if len(linea) > 0:
						lineas_texto.append(limpiar_linea(linea))

				with open(pathapp + "data/txtlimpios/" + line, 'a') as fwrite:
					fwrite.writelines(lineas_texto)
					#.encode('latin-1')
			except:
				continue

		if conteo in [1,2, 10, 50, 100, 500, 800, 1000,1500,2000,2500]:
			print(conteo)
	print datetime.datetime.now()