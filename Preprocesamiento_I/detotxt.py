#!/usr/bin/env python
# -*- coding: utf- 8 -*-
"""
Primera rutina  que sirve para convertir las archivos a txt y generar el listado en 
data/nombres.txt
siguiente legibilidad.py
"""
import tika
import sys
import argparse
from os import walk
import os
import shutil





parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
args = parser.parse_args()


pathapp = os.getcwd()
pathapp = pathapp[0:len(pathapp) - 18]
#print(parser.parse_args())
print(os.getcwd())
#exit()

if args.file ==None:
	print ("Debe digitar la ruta -f [ruta]")
	exit()

exit()
if args.verbose:
    print ("depuración activada!!!")

if args.file:
  print ("El nombre de la carpeta a procesar es: ", args.file)


#print(os.getcwd())	

ruta = args.file
tika.initVM()
from tika import parser



with open( pathapp+"data/nombres.txt", 'a') as fwrite:
	
	for (path,ficheros,archivos) in walk(ruta):
		dirrec= path[len(ruta) +1 :len(path)]
		if not os.path.exists(pathapp + "data/txt/"+dirrec):
			os.mkdir(pathapp + "data/txt/"+dirrec )
			os.mkdir(pathapp + "data/txtlimpios/"+dirrec )
		for archivo in archivos:
		 	(nombre,extencion)=os.path.splitext(archivo)
			nombre=nombre.replace(" " ,"_")
			#print extencion
			if extencion!= ".txt":
				if os.path.getsize(path +"/"+ archivo) != 0:
					parsed =parser.from_file(path +"/"+ archivo)
					#print (parsed["metadata"])
					#print (parsed["content"].encode(sys.stdout.encoding, errors='replace'))
					if not parsed["content"]  is None:
						artxtdata=open(pathapp + "data/txt/" +dirrec+ "/" +nombre + ".txt","w")
						artxtdata.writelines(parsed["content"].encode('utf-8'))
						artxtdata.close
					else:
						shutil.copy(path +"/"+ archivo, pathapp + "data/txt/error/" + archivo )
					#artxmeta=open(path +"/" + nombre + "meta.txt","w")
					#artxmeta.writelines(parsed["metadata"])
					#artxmeta.close
				#print (dirrec)
				if dirrec=="":
					T=  nombre + ".txt\n"
				else:
					T= dirrec +"/"+ nombre + ".txt\n"
			#print(T)
				fwrite.write(T)

			
fwrite.close
