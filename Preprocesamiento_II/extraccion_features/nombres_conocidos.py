
import re
import pandas as pd
from nltk import ngrams

#Diccionario de nombres



with open("/home/figo/Documentos/EJER/pronombres.txt",'r') as k:
	txt=k.read()



pronombres=['adonde', 'adónde', 'algo', 'alguien', 'alguna', 'algunas', 'alguno', 'algunos', 'ambas', 'ambos', 'aquel', 'aquél', 'aquella', 'aquélla', 'aquellas', 'aquéllas', 'aquello', 'aquellos', 'aquéllos', 'bastante', 'bastantes', 'como', 'cómo', 'conmigo', 'consigo', 'contigo', 'cual', 'cual', 'cuál', 'cuales', 'cuáles', 'cualesquiera', 'cualquiera', 'cuando', 'cuándo', 'cuanta', 'cuánta', 'cuantas', 'cuántas', 'cuanto', 'cuánto', 'cuantos', 'cuántos', 'cuya', 'cuyas', 'cuyo', 'cuyos', 'demás', 'demasiada', 'demasiadas', 'demasiado', 'demasiados', 'donde', 'dónde', 'él', 'ella', 'ellas', 'ello', 'ellos', 'esa', 'ésa', 'esas', 'ésas', 'ese', 'ése', 'eso', 'esos', 'ésos', 'esta', 'ésta', 'estas', 'éstas', 'este', 'éste', 'esto', 'estos', 'éstos', 'estotra', 'estotro', 'idem', 'ídem', 'la', 'las', 'le', 'les', 'lo', 'lo', 'los', 'me', 'media', 'medias', 'medio', 'medios', 'mí', 'misma', 'mismas', 'mismo', 'mismos', 'mucha', 'muchas', 'mucho', 'muchos', 'nada', 'nadie', 'ninguna', 'ningunas', 'ninguno', 'ningunos', 'nos', 'nosotras', 'nosotros', 'os', 'otra', 'otras', 'otro', 'otros', 'poca', 'pocas', 'poco', 'pocos', 'qué', 'que', 'qué', 'quien', 'quién', 'quienes', 'quiénes', 'quienesquiera', 'quienquier', 'quienquiera', 'se', 'sí', 'tal', 'tales', 'tanta', 'tantas', 'tanto', 'tantos', 'te', 'ti', 'toda', 'todas', 'todo', 'todos', 'tú', 'una', 'unas', 'uno', 'unos', 'usted', 'ustedes', 'varias', 'varios', 'vos', 'vosotras', 'vosotros', 'yo']
preposiciones=["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde","en", "entre", "hacia", "hasta", "para", "por", "según","segun", "sin","so", "sobre", "tras", "durante", "mediante", "versus" ,"via"]
articulos=["la, el, lo, su , a , sobre, de, los, las, suyo, su, sus, este, aquél, ese, mi, tu, nuestro, vuestro"]
conjunciones=['a', 'condición', 'de', 'que', 'a', 'menos', 'que', 'a', 'pesar', 'de', 'todo', 'a', 'pesar', 'de', 'además', 'de', 'además', 'adonde', 'adonde', 'quiera', 'que', 'ahora', 'que', 'antes', 'que', 'aún', 'así', 'aún', 'cuando', 'aunque', 'como', 'si', 'como', '(causa)', 'como', '(modo)', 'con', 'tal', 'que', 'cualquiera', 'que', 'sea', 'cuando', '(simultaneidad)', 'cuando', 'de', 'lo', 'contrario', 'desde', 'que', 'después', 'que', 'donde', 'donde', 'quiera', 'que', 'en', 'cuanto', 'hasta', 'que', 'lo', 'mismo', 'que', 'mientras', 'mientras', 'que', 'no', 'obstante', 'o', 'para', 'para', 'que', 'pero', 'por', 'por', 'miedo', 'a', 'por', 'mucho', 'que', 'por', 'muy', 'por', 'si', 'porque', 'puesto', 'que', 'si', 'siempre', 'que', 'sin', 'embargo', 'suponiendo', 'que', 'tan', 'pronto', 'como', 'una', 'vez', 'que', 'y', 'ya', 'que']


dic = pd.read_csv('DICCIONARIO.csv', sep=';')
listan = []
for columna in dic.columns:
	listan.append(dic[columna].values.tolist())

listan2=listan[0]+listan[1]+listan[2]
listan3=[str(x) for x in listan2] 

listica= [x.lower() for x in listan3]


def todos_nombres(lista):
		for item in lista:
			if item not in listica:
				return False
		return True

def nombres_conocidos(texto):
	rta=[]
	entrevista = texto.lower()
	for n in {3,4,5}:
		gramas = ngrams(entrevista.split(), n)
		for x in gramas:
			if todos_nombres(x):
				rta.append(" ".join(x))
	return rta
	
with open("/home/figo/Documentos/EJER/Entrevistas_Limpias/0776-03_Entrevista_militar.txt", 'r') as k:
	texto = k.read()
	print(nombres_conocidos(texto))
	


 

