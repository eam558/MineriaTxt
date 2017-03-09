#!/usr/bin/env python
# _*_ coding: utf-8 _*_

from collections import Counter
import json
import os
import sys


# ajusto el sistema a utf8
reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')

pathapp = os.getcwd()
#print(pathapp)
pathapp = pathapp[0:len(pathapp) - 13]

with open( pathapp + "data/json/features_documentos_nuevo.json",'r') as f:
  x=json.load(f)

def dicc_frentes_actividades():

  dicc={}

  frentes=[]
  for en in x["entrevistas"]:
    frentes.append(en["frente"])
  frentes=set(frentes)
  actividades=[]

  for key in x["entrevistas"][0]["finanzas"].keys():
    actividades.append(key)

  for key in x["entrevistas"][0]["delitos"].keys():
    actividades.append(key)

  for key in x["entrevistas"][0][u"política_sociales"].keys():
    actividades.append(key)

  for key in x["entrevistas"][0]["organizacion_logistica"].keys():
    actividades.append(key)

  actividades=list(set(actividades))

#inicialización
  for frente in frentes:
    dicc[frente]={}
    for ac in actividades:
      dicc[frente][ac]=0


  for e in x["entrevistas"]:
    frente=e["frente"]
    if frente!='':
      for ac in e["finanzas"].keys():
        dicc[frente][ac]+=len(e['finanzas'][ac])
      for ac in e["delitos"].keys():
        dicc[frente][ac]+=len(e['delitos'][ac])
      for ac in e[u"política_sociales"].keys():
        dicc[frente][ac]+=len(e[u'política_sociales'][ac])
      for ac in e["organizacion_logistica"].keys():
        dicc[frente][ac]+=len(e['organizacion_logistica'][ac])

  dicc_actividades={}
  for frente in frentes:
    dicc_actividades[frente]=dict(Counter(dicc[frente]).most_common(7))
    

  return dicc_actividades

dicc={"name":"Grafo Frentes",
      "children":[]}

dicc_frentes=dicc_frentes_actividades()

for frente in dicc_frentes.keys():
    dic_temp={"name":frente, "children":[]}
    for act in dicc_frentes[frente].keys():
      dic_temp["children"].append({"name":act,"size":dicc_frentes[frente][act]})
    dicc["children"].append(dic_temp)

with open( pathapp + "data/json/frentes_grafo.json", 'w') as json_file:
  json.dump(dicc, json_file, indent= 4, ensure_ascii=False)
        

