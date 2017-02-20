import re
import pandas as pd
from nltk import ngrams
import json


###################################################################################
#Diccionarios
###################################################################################



###################################################################################
#Diccionarios
###################################################################################


#Diccionario de nombres

dic = pd.read_csv('DICCIONARIO.csv', sep=';')
listan = []
for columna in dic.columns:
	listan.append(dic[columna].values.tolist())

listan2=listan[0]+listan[1]+listan[2]
listan3=[str(x) for x in listan2] 

listica= [x.lower() for x in listan3]

#Diccionario de lugares

df = pd.read_csv("DivisionPoliticoAdministrativaColombia.csv", sep=',')
	
pueblos=list(df["Cabeceras y Centros Poblados"])
for pueblo in pueblos:
	if pueblo=="Colombia":
		pueblos.remove(pueblo)

#Diccionario de género

dic = ['Hombre', 'hombre', 'Mujer', 'mujer', 'Masculino', 'masculino', 'femenino', 'Femenino']

#Diccionario de palabras clave

delitos = {'cirugía': ['cirugía', 'cirugia'], 'abuso': ['abuso', 'abusar'], 'sexo': ['sexo', 'sexual'],
'violación': ['violacion', 'violación', 'biolacion', 'biolación', 'violar','violaron','violó'], 'maltrato': ['maltrato', 'maltratar'],
'cruel': ['cruel'],'acoso': ['acoso', 'acosar'],'retén': ['reten', 'retén','retenes'],'vacuna': ['bacuna', 'vacuna', 'vacunar','vacunas'],
'prisionero': ['prisionero','prisioneros'], 'rapto': ['rapto', 'raptar','rapta','raptar'],'toma': ['toma de', 'tomar de'], 'retención': ['retencion', 'retención'], 
'secuestro': ['secuestro', 'secuestrar','secuestrado','secuestrada','rehen', 'rehén','retenido', 'retener','retenidos'],
'extorsión':['extorsion', 'extorcion', 'extorsión', 'extorción', 'extorsionar'], 'aporte': ['aporte', 'aportar'],
'desaparición': ['desaparicion', 'desaparision', 'desaparición', 'desaparisión', 'desaparecer'], 'matar': ['matar'],
'fosa': ['foza', 'fosa'], 'tumba': ['tumba', 'tumbar'], 'desmembrar': ['desmembrar'], 'descuartizar': ['descuartizar', 'descuartisar'],
'desaparecido': ['desaparecido'], 'caza': ['caza', 'cazar'], 'antipersona': ['antipersona'],
'concejo de guerra': ['consejo de guerra', 'concejo de guerra'], 'torturar': ['torturar'], 'ajusticia': ['ajusticia', 'ajusticiar', 'ajustisia'],
'boleteo': ['boleteo'], 'emboscada': ['emboscada', 'emboscar'],'combate': ['comate', 'combatir'], 'ataque': ['ataque', 'atacar'],
'incursión': ['incursion', 'incursión', 'incurción', 'incurcion', 'incursionar'],'aniquilar': ['aniquilar', 'aniquilamiento'], 'explosivo': ['explosivo', 'explocivo', 'explosibo', 'explocibo', 'explotar'],
'minado': ['minado', 'minar'], 'tatuco': ['tatuco'], 'asesinar': ['asesinar'], 'dar de baja': ['de baja', 'de bajar'], 'enterrar': ['enterrar'],
'disparo': ['disparo', 'disparar'], 'tiro': ['tiro', 'tirar'], 'ejecutar': ['ejecutar'], 'oleoducto': ['oleoducto','oleoductos'],
'hostigar': ['hostigar', 'ostigar', 'hostigamiento'], 'balacera': ['balacera', 'balasera'], 'virgen': ['virgen', 'vírgen', 'virgin'],
'menor de edad': ['niña', 'niño', 'menor', 'menor de', 'menor de edad'], 'mujer': ['mujer']}

politica_sociales = {"ong":["ong", "ONG", "o.n.g", "O.N.G"],
"política":["política","politica","político","politico","politicos","políticos"],
"policía":["policía","policia","policías","policias"], "marcha":["marchas", "marcha"],
"gobernador":["gobernador","gobernadora","gobernadores", "gobernación", "gobernacion","gobierno"], 
"presidente":["presidente", "presidencia", "presidentes","presidencia"], 
"organismo":["organismo","organismos"],
"corregimiento":['corregimiento','corregimientos'],
"milicias":['miliciano','milicias', "milicia", "miliciana"],
"venezuela":["Venezuela", "venezuela"], "ecuador":["ecuador","Ecuador"],
"frontera":['frontera',"fronteras"],
"alcalde":["alcalde", "alcaldes","alcaldía", "alcaldia", "alcaldias", 'alcaldías']
}

organizacion_logistica={
"cartucho":["cartuchos", "cartucho"], 
"cañón" : ["cañon", "cañones", "cañón"], 
"gatillo" : ["gatillos", "gatillo"],  
"ak-47" : ["ak-47", "ak\.47", "ak.47.", "kalashnikov", "kalasnikov"], 
"fusil" : ["fusil", "fusiles"], 
"proveedores" : ["proovedor", "proveedores"],
"pistola" : ["pistolas", "pistola"], 
"granada" : ["granadas", "granada"], 
"mortero" : ["morteros", "mortero"], 
"galil" : ["galiles","galil"], 
"armamento" : ["harmamento", "harmamentos", "armamento", "armamentos"], 
"dotación" : ["dotaciones", "dotacion", "dotación"], 
"municiones" : ["munición", "municion", "municiones"], 
"revólver": ["revolveres", "revolver", "revólver"], 
"fierro" : ["fierros", "fierro"], 
"shotgun" : ["changó", "chango", "shotgun"], 
"chuzo" : ["chuzos", "chuzo"], 
"puñal" : ["punales", "punal", "puñal", "puñal"], 
"navaja" : ["nabajas", "nabaja", "navajas", "navaja"], 
"arma blanca" : ["armas blancas", "armas blanca", "arma blancas", "arma blanca"], 
"petardo" : ["petardos", "petardo"],
"bazuca" : ["bazucas", "bazooca", "bazuca"], 
"bala":["valas", "vala", "balas", "bala"], 
"bisturí" : ["visturi", "visturí", "bisturi", "bisturí"], 
"cuchillo" : ["cuchillos", "cuchillo"], 
"machete" : ["machetes", "machete"], 
"bomba" : ["bombas", "bomba"], 
"explosivos" : ["explosivos", "explosivo"], 
"mina quiebrapatas" : ["minas quiebrapatas", "quievrapatas", "quiebrapatas"], 
"cambuche" :["camvuches", "camvuche", "cambuches", "cambuche"], 
"campamento" : ["campamentos", "campamento"], 
"trinchera" : ["trincheras", "trinchera"], 
"refugio" : ["refujios", "refujio", "refugios", "refugio"], 
"resguardo" : ["resguardos", "resguardo"], 
"cuartel" : ["cuarteles", "cuartel"], 
}

finanzas = {'café':['café','cafe','cafés'],'oro':['oro'],'maíz':['maíz','maiz'],
'fuente':['fuente','fuentes'],'metal':['metal'],'pepas':['pepas','pepa'],
'kilo':['kilo','kilos'],'millón':['millón','millon','millones'],'pancoger':['pangcoger'],
'dolar':['dolares','dólares','dolar','dólar'],'peso':['peso','pesos'],'finca':['finca','fincas'],
'tierra':['tierra','tierras'],'ganadería':['ganado','ganadero','ganadería','ganaderia','ganadera''res','reses','vaca','vacas'],
'económico':['económico','economico','economica','económica','económicos','economicos','económicas','economicas'],
'oxidada':['oxidada','oxidado'],'animal':['animal','animales'],'cultivo':['cultivos','cultivo','siembra'],
'maracachafa':['maracachafa'],'amapola':['amapola','amapolas'],'cristal':['cristal','cristales'],
'clorhidrato':['clorhidrato'],'euro':['euros','euro'],'carbón':['carbón','carbon'],'coltan':['coltán','coltan'],
'minería':['mina','minas','minería','mineria'],'inversión':['inversión','inversion','inversiones'],
'dinero':['dinero','dineros'],'plata':['plata'],'vehículos':['vehículo','vehiculo','vehículos','vehiculos'],'droga':['droga','drogas'],
'narcotráfico':['narcotráfico','narcotrafico','narco'],'raspachín':['raspachin','raspachín','raspachines'],
'laboratorio':['laboratorio','laboratorio'],'recolección':['recolección','recoleccion','recolecta'],
'pisada':['pisada'],'procesamiento':['procesamiento','procesar','procesado','procesada'],
'químico':['químico','químicos','quimico','quimicos'],'secuestro':['secuestro','secuestros'],
'vacuna':['vacuna','vacunas','aporte','aportes','impuesto','impuesta','impuestos'],'extorsión':['extorsión','extorsion','extorsiones','cuotas','cuota'],
'fondos':['fondos'],'lucro':['lucro'],'sueldo':['sueldo','salario'],'paga':['paga','pago'],'remuneración':['remuneración','remuneracion'],
'boleteo':['boleteo'],'porcentaje':['porcentaje'],'coca':['cocaína','cocaina','base de coca','base','pasta de coca','coca'],
'soborno':['soborno','sobornos','soborna'],'robo':['robo','robos','hurto','hurtos'],'casa':['casa','casas'],
'venta':['venta','ventas'],'hectárea':['hectárea','hectáreas','hectarea','hectareas'],'parcela':['parcela','parcelas'],
'fanegada':['fanegadas','fanegada'],'monto':['monto','montos'],'mensual':['mensual','mensualmente','mes'],
'negocio':['negocio','negocios'],'tienda':['tiendas','tiendas'],'deuda':['deuda','deudas'],'remesa':['remesa','remesas'],
'caleta':['caleta','caletas','encaleta','encaletar','encaletamos'],'entierro':['entierro','entierros'],
'tráficante':['traficante','traficantes'],'tráfico':['tráfico'],'negociación':['negociación'],
'empresa':['empresa','empresario','empresarios'],'marihuana':['marihuana']
}


###################################################################################
#Funciones
###################################################################################




###################################################################################
#Features básicos
###################################################################################


def alias(texto):
	palabras=texto.split()
	dicc=["apodos", "Apodos", "alias", "Alias", "apodo", "Apodo"]
	copia_val=[texto.find(x) for x in dicc]
	ind_val=list(filter(lambda x: x>=0, copia_val))
	if len(ind_val) == 0:
		return "No se encuentra alias"
	else:
		menor=min(ind_val)

	palabras_tope=["cargo", "Cargo","lugar", "información","estado","documento","nombre","edad","nivel", "datos", "generales", "nacionalidad", "Lugar", "Información","Estado","Documento","Nombre","Edad","Nivel", "Datos", "Generales", "Nacionalidad","nombres", "Nnombres"]
	ind_tope=[texto.find(x) for x in palabras_tope]
	tope_positiva=list(filter(lambda x: x>menor, ind_tope))
	if len(tope_positiva) == 0:
		return texto[menor:menor+50]
	else:
		tope=min(tope_positiva)
		if (tope-menor)>50:
				return texto[menor:menor+50]
		return texto[menor:tope]

def grupo_arm(texto):
	try:
		grupos = re.findall('( auc|farc|fuerzas armadas revolucionarias|ejercito de liberación |autodefensas|auc |f.a.r.c| far |eln|e\.l\.n)',texto.lower())
		return grupos[0]
	except:
		return ''

def frente(texto):
	try:
		frente= re.findall('frente [0-9]+|[0-9]+ frente|frente combatienes|frente acacio|frente victor|frente vladimir|frente amazonico|frente amazónico|frente urias|frente tulio|frente cacique|frente reinaldo|frente policarpa|frente mario|frente manuela|frente manuel |frente joselo|frente felipe|frente esteban|frente domingo|frente camilo|frente aurelio|frente antonio|frente abelardo',texto.lower())[0]
		if re.findall('[0-9]+',frente)!=[]:
			frente = "frente "+ re.findall('[0-9]+',frente)[0]
		return frente
	except:
		return ''

def cargo(texto):
	try:
		words = re.findall(r'\w+',texto)
		pal = [x.lower() for x in words]
		index = min(pal.index('cargo'),pal.index('desempeñaba'))
		alrededor = pal[index:index+8]
		return(' '.join(alrededor))
	except:
		return ''

def edad(texto):
	entrevista = texto.lower()

	try:
		return re.search('\d\d\sedad', entrevista).group(0)
	except:
		try:
			return re.search('edad\s\d\d', entrevista).group(0)
		except:			
			try: 
				return re.search('años\s\d\d', entrevista).group(0)
			except:
				try: 
					return re.search('\d\d\saños', entrevista).group(0)
				except:
					try:
						
						stri=str(re.search('fecha.+nac.+\d+.+\d+.+\d+', entrevista).group(0))
						año_nac= int(re.search('\d{4}', stri).group(0))
						edad=2016-año_nac
						return edad
					except:
						return ''


def lugar_entrega(texto):
	palabras = texto.split()
	for palabra in palabras:
		if palabra in pueblos:
			return palabra

def todos_nombres(lista):
		for item in lista:
			if item not in listica:
				return False
		return True

def get_nombre_entrevistado(texto):
	entrevista = texto.lower()
	for n in {3,4,5}:
		gramas = ngrams(entrevista.split(), n)
		for x in gramas:
			if todos_nombres(x):
				return " ".join(x)
				
def genero(texto):
	entrevista = texto.lower()

	ind_dic=[entrevista.find(x) for x in dic]

	param = list(filter(lambda x: x>=0, ind_dic))
	if param == []:
		return ''
		
	else:
		menor = min(param)
		ind = ind_dic.index(menor)
		return dic[ind]

def lugar_naci(texto):
	diccionario_inicio=["lugar de nacimiento","nacido en", "oriundo de", "ciudad de", "nacimiento","fecha"]
	ind_dicc=[texto.find(x) for x in diccionario_inicio]
	dicc_positivo=list(filter(lambda x: x>=0, ind_dicc))
	if dicc_positivo==[]:
		return "No se encontró"
	menor=min(dicc_positivo)	
	palabras_nuevas= texto[menor:].split()
	for palabra in palabras_nuevas:
		if palabra in pueblos:
			return palabra


###################################################################################
#Features complejos
###################################################################################

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
					rta.append(" ".join(parrafo[contador-25:contador+26]))
				elif contador<25:
					rta.append(" ".join(parrafo[contador-25:]))	
			elif contador<25:
				if tam-contador >=25:					
					rta.append(" ".join(parrafo[:contador+26]))		
				elif tam-contador < 25:
					rta.append(" ".join(parrafo))
	return rta		

def buscar_palabra(texto, palabra):
	rta=[]
	parrafos= texto.split(".\n")
	for parrafo in parrafos:
		if parrafo.find(" "+palabra+" ")>-1:
			if len(parrafo.split("\n"))>7:
				rta += extraccion_parrafo(parrafo, palabra)
			else: rta+=[parrafo]
	return rta	

def get_delitos(texto):
	out = {}
	for key in delitos.keys():
		palabras_clave = delitos[key]
		parrafos = []
		for palabra in palabras_clave:
			parrafos += buscar_palabra(texto, palabra)
		out[key] = parrafos

	return out 

def get_finanzas(texto):
	out = {}
	for key in delitos.keys():
		palabras_clave = delitos[key]
		parrafos = []
		for palabra in palabras_clave:
			parrafos += buscar_palabra(texto, palabra)
		out[key] = parrafos

	return out 

def get_politica_sociales(texto):
	out = {}
	for key in delitos.keys():
		palabras_clave = delitos[key]
		parrafos = []
		for palabra in palabras_clave:
			parrafos += buscar_palabra(texto, palabra)
		out[key] = parrafos

	return out 

def get_organizacion_logistica(texto):
	out = {}
	for key in delitos.keys():
		palabras_clave = delitos[key]
		parrafos = []
		for palabra in palabras_clave:
			parrafos += buscar_palabra(texto, palabra)
		out[key] = parrafos

	return out 



with open("/home/sorankua/Documentos/proyectos/docs_sala_de_crisis/data/nombres.txt", 'r') as f:
	nombres = [x.strip() for x in f.read().split('\n') if len(x.strip())>0]


###################################################################################
#Features complejos
###################################################################################

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
					rta.append(" ".join(parrafo[contador-25:contador+26]))
				elif contador<25:
					rta.append(" ".join(parrafo[contador-25:]))	
			elif contador<25:
				if tam-contador >=25:					
					rta.append(" ".join(parrafo[:contador+26]))		
				elif tam-contador < 25:
					rta.append(" ".join(parrafo))
	return rta		

def buscar_palabra(texto, palabra):
	rta=[]
	parrafos= texto.split(".\n")
	for parrafo in parrafos:
		parrafo=parrafo.replace(",", " , ").replace(".", " . ").replace("¿", " ¿ ").replace("?", " ? ").replace("(", " ( ").replace(")", " ) ")
		if parrafo.find(" "+palabra+" ")>-1:
			if len(parrafo.split("\n"))>7:
				rta += extraccion_parrafo(parrafo, palabra)
			else: rta+=[parrafo]
	return rta	

def get_delitos(texto):
	out = {}
	for key in delitos.keys():
		palabras_clave = delitos[key]
		parrafos = []
		for palabra in palabras_clave:
			parrafos += buscar_palabra(texto, palabra)
		out[key] = parrafos

	return out 

def get_finanzas(texto):
	out = {}
	for key in finanzas.keys():
		palabras_clave = finanzas[key]
		parrafos = []
		for palabra in palabras_clave:
			parrafos += buscar_palabra(texto, palabra)
		out[key] = parrafos

	return out 

def get_politica_sociales(texto):
	out = {}
	for key in politica_sociales.keys():
		palabras_clave = politica_sociales[key]
		parrafos = []
		for palabra in palabras_clave:
			parrafos += buscar_palabra(texto, palabra)
		out[key] = parrafos

	return out 

def get_organizacion_logistica(texto):
	out = {}
	for key in organizacion_logistica.keys():
		palabras_clave = organizacion_logistica[key]
		parrafos = []
		for palabra in palabras_clave:
			parrafos += buscar_palabra(texto, palabra)
		out[key] = parrafos

	return out 

with open('/home/sorankua/Documentos/proyectos/docs_sala_de_crisis/preprocesamiento/extraccion_features/alias_conocidos.txt') as f:
	texto_alias = f.read()

alias_entrevistas = texto_alias.split('//')

def alias_conocidos(archivo):
	dicc_temp = {}	
	for ent in alias_entrevistas:
		lineas = [lin for lin in ent.split('\n') if len(lin.strip())>0]
		nombre_entrevista = lineas[0]
		if archivo == nombre_entrevista:
			del lineas[0]
			if len(lineas)>0:
				for linea in lineas:
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
					dicc_temp[alias]['tipo']=tipo
					dicc_temp[alias]['frente']=frente
	return dicc_temp


with open('/home/sorankua/Documentos/proyectos/docs_sala_de_crisis/preprocesamiento/extraccion_features/conocidos.txt') as f:
	texto_nombres = f.read()

nombres_entrevistas = texto_nombres.split('//')

def nombres_conocidos(archivo):
	nombres_conocidos = []
	for ent in nombres_entrevistas:
		lineas = [lin for lin in ent.split('\n') if len(lin.strip())>0]
		nombre_entrevista = lineas[0]
		if archivo == nombre_entrevista:
 			del lineas[0]
 			nombres_conocidos= lineas
	return nombres_conocidos



def archivo_JSON(archivo):
	with open("/home/sorankua/Documentos/datos_limpios/"+archivo, 'r') as k:
		texto = k.read()
	js={ 
		"nombre_archivo": archivo,
		"nombre_entrevistado":get_nombre_entrevistado(texto),
		"alias": alias(texto),
		"grupo_armado":grupo_arm(texto),
		"frente": frente(texto),
		"edad": edad(texto),
		"lugar_desmovilizacion" : lugar_entrega(texto),
		"cargo": cargo(texto),
		"genero": genero(texto),
		"lugar_nacimiento": lugar_naci(texto),
		"delitos": get_delitos(texto),
		"finanzas": get_finanzas(texto),
		"organizacion_logistica": get_organizacion_logistica(texto),
		"política_sociales": get_politica_sociales(texto),
		"alias_conocidos":alias_conocidos(archivo),
		"nombres_conocidos":nombres_conocidos(archivo)
	}
	
	return js


diccionario_json=[]
with open("/home/sorankua/Documentos/proyectos/docs_sala_de_crisis/data/nombres.txt", 'r') as f:
	archivos = f.read().split('\n')

"""
conta=0
for archivo in archivos:
	print(archivo_JSON(archivo)['nombres_conocidos'])
	#conta+=archivo
	print(archivo)
"""
conteo=0
for archivo in archivos:
	diccionario_json.append(archivo_JSON(archivo))
	conteo+=1
	if conteo in [1,7,57,165,255,567,831,1000]:
		print(conteo)
	#print(archivo)

out={"entrevistas":diccionario_json}

with open('features_documentos_nuevo.json', 'w', encoding='utf8') as json_file:
	json.dump(out, json_file, indent= 4, ensure_ascii=False)

