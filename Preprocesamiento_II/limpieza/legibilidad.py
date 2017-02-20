import re
import numpy as np
from sklearn.cluster import KMeans

def consonantes_seguidas(word): #sin vocales
    if re.search("[A-zñ]{4}", word) and re.search("[^aeiouAEIOU]{4}", word):
        return 1
    else:
        return 0

def vocales_seguidas(word): #sin vocales
    if re.search("[aeiouAEIOU]{4}", word):
        return 1
    else:
        return 0
    
def error1(word): #dada una palabra la separa en subpalabras para calcular error1
    subpalabras = [word[i:i+4] for i in range(len(word)-3)]
    lista_conteos = list(map(lambda x: consonantes_seguidas(x), subpalabras))
    return sum(lista_conteos)

def error2(word): #dada una palabra la separa en subpalabras para calcular error1
    subpalabras = [word[i:i+4] for i in range(len(word)-3)]
    lista_conteos = list(map(lambda x: vocales_seguidas(x), subpalabras))
    return sum(lista_conteos)

def error3(word): #mayuscula despues de minuscula
    lista_errores = re.findall("([a-zñ])(?=[A-Z])\w", word)
    return len(lista_errores)

def error4(word): #numeros entre letras
    lista_errores = re.findall("([0-9][a-zñA-Z]+)|([a-zñA-Z][0-9])", word)
    return len(lista_errores)


def error5(sentence): #contar separacion entre letras
    trial = [x.strip() for x in sentence.split()]
    subpalabras = [trial[i:i+3] for i in range(len(trial)-2)]
    contador = 0

    for s in subpalabras:
        if sum(list(map(lambda x: len(re.findall("[A-zñ]", x)), s))) == 3:
            contador +=1

    return contador

def error6(word):
    lista_errores = re.findall("([^a-zñA-Z0-9])+",word)
    return len(lista_errores)

def get_legibilidad(texto):
    lista_palabras = [x.strip() for x in texto.split()]

    errores1 = sum([error1(x) for x in lista_palabras])
    errores2 = sum([error2(x) for x in lista_palabras])
    errores3 = sum([error3(x) for x in lista_palabras])
    errores4 = sum([error4(x) for x in lista_palabras])
    errores5 = error5(texto)
    errores6 = sum([error6(x) for x in lista_palabras])

    vector_errores = np.array([errores1, errores2, errores3, errores4, errores5, errores6], dtype=np.float)
    if len(texto.split()) != 0:
        scores = vector_errores/float(len(texto.split()))
    else:
        scores = np.array([0, 0, 0, 0, 0, 0])

    return scores

matriz_scores = []
with open("nombres_archivos_limpios.txt", 'r') as f:
    lines = f.readlines()
    nombres_archivos = [x.strip() for x in lines if len(x.strip()) > 0]
    for line in nombres_archivos:
        try:
            with open("clean_data/" + line, 'r') as fread:
                text = fread.read()
                if max(list(get_legibilidad(text))) != 0:
                    matriz_scores.append(list(get_legibilidad(text)))
        except:
            continue
            
matriz_scores = np.array(matriz_scores)

for k in range (3, 7, 1):
    kmeans = KMeans(n_clusters=k).fit(matriz_scores)
    nro_cluster = np.array(kmeans.labels_, dtype=np.int32).reshape((matriz_scores.shape[0], 1))

    matriz_clusters = np.hstack((matriz_scores, nro_cluster))


    with open("scores_limpios"+str(k)+".txt",'a') as fwrite:
        print("nombre_archivo,score1,score2,score3,score4,score5,score6,nro_cluster", file=fwrite)
        for i in range(matriz_clusters.shape[0]):
            print(nombres_archivos[i] + "," + str(matriz_clusters[i][0]) + "," + str(matriz_clusters[i][1]) + "," + str(matriz_clusters[i][2]) + "," + str(matriz_clusters[i][3]) + "," + str(matriz_clusters[i][4]) + "," + str(matriz_clusters[i][5]) + "," + str(matriz_clusters[i][6]), file=fwrite)


"""


doc = 'ash \n asdjasdj \n \n ejej'

#Abrir documento
posibles = ['mbox-short.txt','romeo.txt','words.txt']
for p in posibles:
    doc = open(p,'r')
    print doc[1]


palabb = [s.strip() for s in doc.split('\n')]
sin_espacio = list(filter(lambda x: len(x)>0,palabb))
texto = ' '.join(sin_espacio)
print texto


#print "Frase de prueba:"
line = 'ppppp3 3p1alAbrA  s cOppmbjjjjia%. #rrR tuui/oiu k i o p o &a ee4er ddRha AARRR <<yy'
palabras = line.split()


s=texte1(line)
p2= list(map(lambda x: error2(x), palabras))
p3= list(map(lambda x: error3(x), palabras))
p5= list(map(lambda x: error5(x), palabras))


#print line 
#print "\nResultados:"
#print "error 1: " + str(sum(s)) #consonantes seguidas
#print "error 2: " + str(sum([len(pi) for pi in p2]))#mayusc despues minusc
#print "error 3: " + str(sum([len(pi) for pi in p3]))#numeros
#print "error 4: " + str(error4(line))#letras separadas
#print "error 5: " + str(sum([len(pi) for pi in p5]))#simbolos raros
#print "error total: " + str(sum(s) +sum([len(pi) for pi in p2])+sum([len(pi) for pi in p3])+error4(line)+sum([len(pi) for pi in p5]))
#print "numero de palabras: " + str(len(palabras))
#print "numero de caracteres: " + str(len(line))


caract=len(line)
error = [float(sum(s))/float(caract), float(sum([len(pi) for pi in p2]))/float(caract), float(sum([len(pi) for pi in p3]))/float(caract),float(error4(line))/float(caract),float(sum([len(pi) for pi in p5]))/float(caract)]

print error



#from sklearn.cluster import KMeans
#import numpy as np
#X = np.array([[1, 2], [1, 4], [1, 0],[4, 2], [4, 4], [4, 0]])
#kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
#kmeans.labels_
#array([0, 0, 0, 1, 1, 1], dtype=int32)
#kmeans.predict([[0, 0], [4, 4]])
#array([0, 1], dtype=int32)
#kmeans.cluster_centers_
#array([[ 1.,  2.],[ 4.,  2.]])


"""