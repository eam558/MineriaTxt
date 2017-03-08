#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import os
import io

import sys
reload(sys)

print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
print sys.getdefaultencoding()
"""
pathapp = os.getcwd()
pathapp = os.getcwd()
print(pathapp)
pathapp = pathapp[0:len(pathapp) - 3]
print(pathapp)
with open( pathapp+"Procesamiento/features_documentos_nuevo.json",'r') as f:
	features = json.load(f)

for x in features['entrevistas']:
    if len(x['frente'].strip()) > 0:
       print x['frente']


"""

with open("grafo_actividades_nuevo.json",'r') as f:
	features = json.load(f)
print features

dicc_total={}
dicc_total['nn']=[]
#dicc_total['nn'].append({"población,torivio, ññññ,ááá,?¿"})
dicc_total['nn'].append({'poblacion':'350' ,'torivio':'256¡¿?', 'cadsa':'rrrññrr'})
print dicc_total
with open('grafo_actividades_nuevo.json', 'w') as json_file:
   json.dump( dicc_total, json_file, indent=4,ensure_ascii=False)