import re 

def conocidos(texto):
	palabras=texto.split()
	dic=["alias","Alias"]
	conocidos=re.findall('([a|A]\.[A-z]+\s[^\.]+?)\.',texto)
	otro = re.findall('[a|A]lias\s[A-z]+ ',texto)
	conocido=re.findall('([a|A]lias\s[A-z]+[^\.]+?)\.', texto)
	todos = conocidos+conocido
	return todos
	
		

with open("/home/figo/Documentos/EJER/nombres.txt", 'r') as f:
	archivos = f.read().split('\n')

for archivo in archivos:
	with open("/home/figo/Documentos/EJER/Entrevistas_Limpias/"+archivo, 'r') as k:
		texto = k.read()
	print(conocidos(texto))		



