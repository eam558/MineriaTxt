#!/usr/bin/env python
#_*_ coding:utf-8 _*_
from __future__ import print_function
import re



#Por Revisar

def quitar_tildes(word):
    return word.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

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
			if ('frente' in element.lower() and rodeado_de_nombre) or 'columna' in element.lower() or 'cuadrilla' in element.lower() or ('compañia' in element.lower() and rodeado_de_nombre):
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
			elif element.lower() == 'compañia': 
				if array[i-1][0] in digitos:
					return "COMPAÑIA "+array[i-1]
				elif array[i+1][0].isupper():
					nombre_estructura = ""
					got_nombre = False
					for word in array[i+1:]:
						if word[0].isupper() and 'alias' not in word.lower():
							nombre_estructura += word
							got_nombre = True
						else:
							if got_nombre:
								return "COMPAÑIA "+ nombre_estructura.upper()
							if 'alias' in word:
								return "COMPAÑIA "+nombre_estructura.upper()
				elif array[i+1][0] in digitos:
					return "COMPAÑIA "+array[i+1]
				else:
					return "COMPAÑIA"
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
	text = text.replace("\n", " // ").replace(",", " , ").replace(".", " . ").replace("¿", " ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")
	words = text.split()
	got_something = False
	done = False
	for i in range(len(words)-10):
		word = words[i:i+10]
		if is_alias(" ".join(word)) and len(extract_alias(word).split()) > 1 and not done:
			alias = extract_alias(word)
			cargo = ""
			estructura = ""
			if has_cargo(word) and has_estructura(word):
				cargo = get_cargo(word)
				estructura = get_estructura(word)
	
				if len(estructura.split()) >1:
					info = (alias, cargo, estructura)
					#info = {"alias": alias, "cargo": cargo, "estructura": estructura}
				else:
					info = (alias, cargo, "")
					#info = {"alias": alias, "cargo": cargo, "estructura": ""}
				done = True
			else:
				if has_cargo(word):
					cargo = get_cargo(word)
					info_tmp = (alias, cargo, "")
					#info_tmp = {"alias": alias, "cargo": cargo, "estructura": ""}
				elif has_estructura(word) and len(get_estructura(word).split()) >1:
					estructura = get_estructura(word)
					info_tmp = (alias, "MIEMBRO", estructura)
					#info_tmp = {"alias": alias, "cargo": "MIEMBRO", "estructura": estructura}
				else:
					info_tmp = (alias, "MIEMBRO", "")
					#info_tmp = {"alias": alias, "cargo": "MIEMBRO", "estructura": ""}
			got_something = True
		else:
			if got_something and not done:
				info = info_tmp
				done = True
		if done:
			ans.append(info)
			got_something = False
			done = False
	return ans
		
#Modificar las rutas en estas instrucciones
#with open("/home/abue/Documents/nombres.txt", 'r') as f:
with open("/home/otaivin/Trabajo/MineriaTxt/data/nombres.txt", 'r') as f:
	archivos = [x.strip() for x in f.read().split('\n') if len(x.strip())>0]

i = 0
with open("alias_conocidos.txt", 'a') as fwrite:
	for archivo in archivos:
		print(archivo,file=fwrite)
		with open("/home/otaivin/Trabajo/MineriaTxt/data/txtlimpios/"+archivo, 'r') as f:
			texto = f.read()
			for alias in set(get_alias_conocidos(texto)):
				print(alias,file=fwrite)
			print("//",file=fwrite)
		i += 1
		if i in [100, 300, 500, 700]:
			print("Van "+str(i))
