import re 

def extraccion_parrafo(pparrafo, palabra):
	parrafo=pparrafo.split()
	contador=0
	tam=len(parrafo)
	
	rta=[]
	for p in parrafo:
		contador+=1
		if p == palabra:
			parrafo_nuevo=''
			if contador>=25:
				if tam-contador >=25:
					#for t in parrafo[contador-25:contador+26]:
					#	parrafo_nuevo+=" "+t
					#	rta.append(parrafo_nuevo)
					rta.append(" ".join(parrafo[contador-25:contador+26]))
				elif contador<25:
					#for t in parrafo[contador-25:]:
					#	parrafo_nuevo+=" "+t
					#	rta.append(parrafo_nuevo)
					rta.append(" ".join(parrafo[contador-25:]))	
			elif contador<25:
				if tam-contador >=25:
					#for t in parrafo[:contador+26]:
					#	parrafo_nuevo+=" "+t
					#	rta.append(parrafo_nuevo)					
					rta.append(" ".join(parrafo[:contador+26]))		
				elif tam-contador < 25:
					#for t in parrafo:
					#	parrafo_nuevo+=" "+t			
					#	rta.append(parrafo_nuevo)
					rta.append(" ".join(parrafo))
	return rta		

def parrafo_final(texto, palabra):
	rta=[]
	parrafos= texto.split(".\n")
	for parrafo in parrafos:
		if parrafo.find(palabra)>-1:
			if len(parrafo.split("\n"))>7:


				rta += extraccion_parrafo(parrafo,palabra)
			else: rta+=parrafo

	return rta		

			
with open("/home/figo/Documentos/EJER/Entrevistas_Limpias/2035-03_Entrevista_militar.txt", 'r') as k:
	texto = k.read()
	print(parrafo_final(texto,"nombre"))




