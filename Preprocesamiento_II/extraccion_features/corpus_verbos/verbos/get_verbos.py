import re
import os
import codecs
import json

letras = ['a', 'a1', 'a2', 'b', 'c', 'c1', 'd', 'd1', 'e', 'e1', 'f', 'g', 'h', 'i', 'j', 'l', 'm','n', 'o', 'p', 'p1', 'q', 'r', 'r1', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
pronombres = ['yo', 'tú', 'él', 'nosotros', 'vosotros', 'ellos', 'me', 'te', 'se', 'nos', 'os']
haber_acompañante = ['he', 'has', 'ha', 'hemos', 'habéis', 'han', 'había', 'habías', 'habíamos', 'habíais','habían', 'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 'habré', 'habrás', 'habrá', 'habremos', 'habréis',  'habrán', 'haya', 'hayas', 'haya', 'hayamos', 'hayáis', 'hayan', 'hubiere', 'hubieres', 'hubiere', 'hubiéremos', 'hubiereis', 'hubieren', 'habría', 'habrías', 'habría', 'habríamos', 'habríais', 'habrían']

def limpiar_palabra(word):
	ans = word.replace("&#225;", "á").replace("&#233;", "é").replace("&#237;", "í").replace("&#243;", "ó").replace("&#250;", "ú").replace("&#241;", "ñ")
	return ans


def get_conjugaciones(url, es_haber):
	ans = []
	html_verbo = re.search("conjugacion\d?/([^<]+?\.html)", url).group(1)
	with codecs.open(html_verbo, 'r' ,encoding='utf-8', errors='ignore') as f:
		bloques = f.read().split('<div class="conjBlock">')[1:]
	for bloque in bloques:
		if bloque == bloques[-1]:
			bloque = bloque[:bloque.find("</div>")]
		bloque = limpiar_palabra(bloque)
		sin_tags = re.sub("<[^<]+?>", " ", bloque)
		sin_tags = re.sub("<!--", "", sin_tags)
		sin_tags = re.sub(".*\(.+?;", "", sin_tags)
		sin_tags = re.sub(".+?-->", "", sin_tags)	
		texto_limpio = re.sub("<script>.+?</script>", "", sin_tags)
		words = set([limpiar_palabra(x) for x in texto_limpio.split() if len(x.strip()) > 0])
		if not es_haber:
			ans += list(filter(lambda x: x not in pronombres and x not in haber_acompañante, list(words)))
		else:
			ans += list(filter(lambda x: x not in pronombres, list(words)))
	ans = list(set(ans))
	return ans

def get_url(text):
	ans = re.search('href=\'(.*?conjugacion[^<]+?html)\'>[a-zñ]+</a>', text).group(1).replace("..", "")
	if not "http://www.vocabulix.com" in ans:
		ans = "http://www.vocabulix.com" + ans
	return ans

def get_verbo(text):
	verbo = re.search('href=\'.*?conjugacion[^<]+?html\'>([a-zñ]+)</a>', text).group(1)
	return verbo


out = {}
lista_verbos = []
for letra in letras:
	with open("/home/carlos/proyectos/work/docs_sala_de_crisis/preprocesamiento/extraccion_features/corpus_verbos/letras/" + letra + "_spanish.html", 'r') as f:
		texto = f.read()
	columnas = texto.split('<div class="indexColumn">')
	columnas = columnas[1:]
	for columna in columnas:
		anclas_verbos_letra = re.findall("href=\'\.\./conjugacion[^<]+?html\'>[a-zñ]+?</a>", columna)
		urls = list(map(lambda x: get_url(x), anclas_verbos_letra))
		verbos = list(map(lambda x: get_verbo(x), anclas_verbos_letra))
		for verbo, url in zip(verbos, urls):	
			if verbo != 'haber':
				conjugaciones = get_conjugaciones(url, False)
			else:
				conjugaciones = get_conjugaciones(url, True)
			obj_verbo = {
				"verbo": verbo,
				"conjugaciones": conjugaciones
			}
			lista_verbos.append(obj_verbo)

out["verbos"] = lista_verbos

with open('conjugaciones.json', 'w', encoding='utf8') as json_file:
    json.dump(out, json_file, ensure_ascii=False)

