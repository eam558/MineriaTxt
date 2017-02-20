import json

with open("conjugaciones.json", 'r') as f:
	data = json.load(f)

def stem(word):
	for verbo in data["verbos"]:
		if word.lower() in verbo["conjugaciones"]:
			if word[0].isupper():
				stemmed_verbo = verbo["verbo"][0].upper() + verbo["verbo"][1:]
				return stemmed_verbo
			else:
				return verbo["verbo"]

	return word

def stem_text(text):
	texto = text.replace(",", " , ").replace(".", " . ").replace("¿", " ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")	
	palabras = texto.split()
	for palabra in palabras:
		texto = texto.replace(" " + palabra + " ", " " + stem(palabra) + " ")
		texto = texto.replace("\n" + palabra + " ", "\n" + stem(palabra) + " ")
		texto = texto.replace(" " + palabra + "\n", " " + stem(palabra) + "\n")
	texto = texto.replace(" , ", ",").replace(" . ", ".").replace(" ¿ ", "¿").replace(" ? ", "?").replace(" ( ", "(").replace(" ) ", ")")
	return texto

with open("nombres.txt", 'r') as f:
	lines = f.readlines()
	nombres_archivos = [x.strip() for x in lines if len(x.strip()) > 0]
	for line in nombres_archivos:
		try:
			with open("datos_limpios/" + line, 'r') as fread:
				texto = fread.read()
			with open("datos_lematizados/" + line, 'w') as fwrite: 
				print(stem_text(texto), file=fwrite)
		except:
			continue
