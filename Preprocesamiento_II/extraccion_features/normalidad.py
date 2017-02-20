import numpy as np
lineas_por_parra_todas_entrevistas=[]

with open("/home/ellobo/Documentos/gen/nombres.txt", 'r') as f:
	archivos = [x.strip() for x in f.read().split('\n') if len(x.strip())>0]

for archivo in archivos:
	with open("/home/ellobo/Documentos/gen/datos_limpios/"+archivo, 'r') as k:
		entrevista_sin_separar = k.read()
	
	
	#Separamos por párrafo. Si se desea por frase quite el "\." del parámetro del split.
	entevista_por_punto = entrevista_sin_separar.split(".")

	lineas_por_parra = []

	for parra in entevista_por_punto:
		parra = parra.strip()
		lineas_por_parra.append(len(parra.split("\n")))

	lineas_por_parra_todas_entrevistas+=lineas_por_parra

lineas_por_parra_todas_entrevistas = np.array(lineas_por_parra_todas_entrevistas)
print(lineas_por_parra_todas_entrevistas)
