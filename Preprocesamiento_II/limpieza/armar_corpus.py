import re
import os

def clean_text(text):
	without_tags = re.sub(r'<[^<]+?>', '', text)
	cleaned_text = re.sub(r'\[.+?\]', '', without_tags)
	return cleaned_text

def get_links(text):
	links_totales = []
	lista_text = re.findall(r'<p id=\"m.+?</p>', text)
	for parrafo in lista_text:
		links = re.findall(r'<a href=\"([^<0-9]+?\.html)\"[^<]*?</a>', parrafo)
		links_acentos = re.findall(r'<a href=\"([^<]+?\%[^<]+?\.html)\"[^<]*?</a>', parrafo)
		links_totales += links
		links_totales += links_acentos

	links_totales = list(set(links_totales))
	return links_totales

def extract_clean_paragraphs(text):
	lista_text = re.findall(r'<p id=\"m.+?</p>', text)
	lista_clean_text = list(map(lambda x: clean_text(x), lista_text))
	return lista_clean_text

def download_articles():
	with open("links_obtenidos.txt", 'r') as fread:
		texto = fread.read()
		links = texto.split('\n')
		for link in links:
			os.system("wget http://localhost:8083/wikipedia/A/"+link.strip()+" -P raw_data/")

def get_final_links():
	links_finales = []

	with open("raw_data_inventory.txt",'r') as f:
		texto = f.read()
		archives = texto.split('\n')
		for archive in archives:
			with open("raw_data/"+archive.strip(),'r') as f:
				text = f.read()
				links_totales = get_links(text)
				links_finales += links_totales

		links_finales = list(set(links_finales))

	return links_finales


def save_clean_articles():
	with open("raw_data_inventory.txt",'r') as f:
		texto = f.read()
		archives = texto.split('\n')
		i = 0
		for archive in archives:
			try:
				if archive.strip()[-1] != '1':
					with open("raw_data/"+archive.strip(),'r') as fread:
						text = fread.read()
						lista_parrafos = extract_clean_paragraphs(text)
					with open("data/"+archive.strip().replace(".html", ".txt"), 'a') as fwrite:
						for parrafo in lista_parrafos:
							print(parrafo, file=fwrite)
			except:
				continue
			i += 1
			if i in [1, 2, 3, 10, 1000, 3000, 5000, 10000, 15000]:
				print("Van "+str(i)+"!!")

save_clean_articles()
