"""
Parte del resumen de los acuerdos de paz bak end
"""
import json

def textos_to_json():
	out = {}
	puntos = {}
	for i in range(7):
		with open("../data/output_punto_"+str(i)+".txt", 'r') as f:
			text = f.read()
			items = text.split('---')

			punto_actual = {}
			resumen = {}
			topicos = {}

			for j in range(3):
				nivel = items[j+2].replace("nivel_"+str(j+1)+":\n", '')
				topico = items[j+6].replace("topicos_"+str(j+1)+":\n", '')
				resumen["nivel_"+str(j+1)] = nivel
				topicos["topicos_"+str(j+1)] = topico

			punto_actual["resumen"] = resumen
			punto_actual["topicos"] = topicos
			puntos["punto_"+str(i)] = punto_actual

	out["puntos"] = puntos

	with open('../data/ejemplo.json', 'w', encoding='utf8') as json_file:
	    json.dump(out, json_file, ensure_ascii=False)


def frecuencias_to_json():
	out = {}
	
	politica = []
	justicia = []
	tierras = []
	posconflicto = []
	reparacion = []

	with open("../data/frecuencias.txt", 'r') as f:
		lines = f.read().split("\n")
		politica = [float(x.split(",")[0]) for x in lines]
		justicia = [float(x.split(",")[1]) for x in lines]
		tierras = [float(x.split(",")[2]) for x in lines]
		posconflicto = [float(x.split(",")[3]) for x in lines]
		reparacion = [float(x.split(",")[4]) for x in lines]

	out["politica"] = politica
	out["justicia"] = justicia
	out["tierras"] = tierras
	out["posconflicto"] = posconflicto
	out["reparacion"] = reparacion

	with open('../data/frecuencias.json', 'w', encoding='utf8') as json_file:
	    json.dump(out, json_file, ensure_ascii=False)






	
	


