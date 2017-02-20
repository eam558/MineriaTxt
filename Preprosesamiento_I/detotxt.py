#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tika
import sys
import argparse
from os import walk
import os


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
args = parser.parse_args()


#if args.verbose:
#    print ("depuración activada!!!")

if args.file:
   print ("El nombre de la carpeta a procesar es: ", args.file)

#if sys.argv[1]=""
	#print ("Debe digitar la ruta -f ")
	

ruta = args.file
tika.initVM()
from tika import parser

#print (ruta)
for (path,ficheros,archivos) in walk(ruta):
#	print ("Ruta" + path)
#	print("carpetas")
#	print ( ficheros)
#	print ("archivos  " )
#	print( archivos [0])
	
	for archivo in archivos:
		print(path + "/" + archivo)
		(nombre,extencion)=os.path.splitext(archivo)
		if extencion!= "txt":
			if os.path.getsize(path +"/"+ archivo) != 0:

				parsed =parser.from_file(path +"/"+ archivo)
				#print (parsed["metadata"])

				
				nombre=nombre.replace(" " ,"_")
				#print (parsed["content"])
				if not parsed["content"]  is None:
					artxtdata=open(path +"/" + nombre + ".txt","w")
					artxtdata.writelines(parsed["content"])
					artxtdata.close
				artxmeta=open(path +"/" + nombre + "meta.txt","w")
				artxmeta.writelines(parsed["metadata"])
				artxmeta.close
	
