with open('/home/serankua/proyectos/docs_sala_de_crisis/preprocesamiento/extraccion_features/alias_conocidos.txt') as f:
	texto = f.read()

alias_entrevistas = texto.split('//')
'0688-03_Entrevista_militar.txt'
def dicc_entrevista_alias(archivo):
	for ent in alias_entrevistas:
		lineas = ent.split('\n')
		nombre_entrevista = lineas[0]
		if archivo == nombre_entrevista:
			dicc_temp = {}			
			for linea in lineas[1:len(lineas)]:
				palabras =linea.replace('(','').replace(')','').replace('\'','').split(',') 
				alias = palabras[0].strip()
				try:
					tipo = palabras[1].strip()
				except:
					tipo =''
				try:
					frente = palabras[2].strip()
				except Exception as e:
					frente = ''

				dicc_temp[alias]={}
				dicc_temp[alias]['tipo']=alias
				dicc_temp[alias]['frente']=frente
	return dicc_temp

dicci=dicc_entrevista_alias('0688-03_Entrevista_militar.txt')

for k in dicci.keys():
	print(k)

print(dicci['alias Darry'])
