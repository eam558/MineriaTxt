import os

os.system("ls > nombres_archivos.txt")
"""with open("nombres_archivos.txt", 'r') as f:
	lines = f.readlines()
	with open("nombres_archivos_filtrados.txt", 'a') as fwrite:
		for line in lines:
			line = line.strip()
			new_name = line.replace(" ", "_")
			if len(new_name.split(".")) == 2 and new_name.split(".")[1] == 'pdf':
				os.system("mv " + line.replace(" ", "\ ") + " " + new_name)
				print(new_name, file=fwrite)

with open("nombres_archivos_convertidos.txt", 'a') as fwrite:
	with open("nombres_archivos_filtrados.txt", 'r') as fread:
		lines = fread.readlines()
		lines = [x.strip() for x in lines if len(x.strip()) > 0]
		for line in lines:
			os.system("pdftotext " + line + " data/" + line.split(".")[0] + ".txt")
			print(line.split(".")[0] + ".txt", file=fwrite)
"""
#os.system("python legibilidad.py")

