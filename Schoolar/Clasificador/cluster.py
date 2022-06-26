import pandas as pd
# librerias para pre-procesamiento
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import davies_bouldin_score
from sklearn import  metrics
#from jqmcvi import base
#librerias para graficar datos
import matplotlib.pyplot as plt
import numpy as np

datos= pd.read_csv('grimms.csv') # lectura del dataframe

#print(datos)

# explorando la informacion

#print(datos.info())

# pre-procesamiento de datos

archivos = datos['Text'].values.astype("U")

#print(archivos)
vectorizacion = TfidfVectorizer(max_df=0.8,stop_words='english', encoding='utf-8')  #Frecuencia de palabras
caracteristicas = vectorizacion.fit_transform(archivos)  #transformando todas las caracteristicas usando la media y la varianza

#print(caracteristicas)

#print(cosine_similarity(caracteristicas[0:62],caracteristicas))

some= caracteristicas.toarray()



k=20
modelo = KMeans(n_clusters=k,init='k-means++',max_iter=100,n_init=1)   # Aplicacion del algoritmo kmenas
#KMeans(No. Clusters, selecciona los centros de clusteres iniciales, maximo de iteraciones del algoritmo, No. de ejecuciones )
modelo.fit(caracteristicas)  #entrenamiento del modelo con los datos


datos['cluster'] = modelo.labels_ #asignacion de las etiquetas

#print(datos.tail())

# resultado al archivo de texto

clusters = datos.groupby('cluster')

#creacion de archivos csv
for cluster in clusters.groups:
    f = open('clusters/cluster'+str(cluster)+'.csv', 'w') # creacion del csv 
    data = clusters.get_group(cluster)[['Title']]     # obtencion de las columnas del titulo y texto
    f.write(data.to_csv(index_label='id'))   # colocamos los datos
    f.close() # finalizacion de la escritura del archivo

#obtencion de los centroides
print('Centroides: \n')

orden_centroides = modelo.cluster_centers_.argsort()[:,::-1]  #ordena las centros de los clusters por proximidad al centroide
terms = vectorizacion.get_feature_names_out()  #obtencion de la salida de los nombres por caracteristicas para la transformacion


#print(orden_centroides)
#print(terms)
# impresion de los centroides
for i in range (k):
    print("Cluster %d: " %i)
    for j in orden_centroides[i,:10]:
         
        print('%s' %terms[j])
        
    print('-----------')


# post

ct = pd.crosstab(datos['Title'],datos['cluster'])

print(ct)

print("Calidad agrupacion: ", modelo.inertia_)
print("Indice Davies Bouldin: ",davies_bouldin_score(some,modelo.labels_))