"""
Obtiene de una entravista el grupo armado
"""

import numpy as np

def get_grupo_armado(text):
	text_lower = text.lower()
	indices = [text_lower.find(" farc "), text_lower.find(" eln "), text_lower.find(" auc ")]
	if max(indices) < 0:
		return "Ninguna de las tres"
	index = np.argmin([x for x in indices if x>0])
	return ["FARC", "ELN", "AUC"][index]

def get_clase_entrevistador(text):
	text_lower = text.lower()
	indices = [text_lower.find(" fiscalia "), text_lower.find(" ejercito "), text_lower.find(" policia ")]
	if max(indices) < 0:
		return "Ninguna de las tres"
	index = np.argmin([x for x in indices if x>0])
	return ["Fiscalía", "Ejército", "Policía"][index]

for i in range(5):
	with open("000"+str(i+1)+"-03_Entrevista_militar.txt",'r') as f:
		texto = f.read()
		print(get_grupo_armado(texto), get_clase_entrevistador(texto))


