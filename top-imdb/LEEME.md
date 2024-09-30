*********************************************************************************************************************

Instrucciones para resolver el problema en linea de comando (EN LINUX)
---------------------------------------------------------------------------------------------------------------------

Vamos a suponer que ya tenemos descomprimido el archivo y ya accedimos a ´el,
por lo que nuestro directorio actual es aclImdb, accedemos al directorio train para estar
en el lugar adecuado para comenzar.

Haremos primero la lista de los 10 peores.

Paso 1.
ls | grep -Eo ’[0-9]+\_[0-9]+\.txt’ |awk -F’[_.]’ ’{print $1, $2}’ | sort -n > ../neg_id_cal.txt

Paso 2.
cd ..

Paso 3.
paste -d’ ’ <(tail -n +1 urls_neg.txt) neg_id_cal.txt | awk ’{print $1, $3}’ > url_cal.txt

Paso 4.
awk ’{ puntos[$1] += $2; suma[$1]++} END { for (url in puntos) print url, puntos[url]/suma[url]}’ url_cal.txt | sort -k2,2n | head -n 10 > promedio_neg.txt

Paso 5.
cat promedio_neg.txt


Haremos ahora la lista de los 10 mejores.

Paso 1.
ls | grep -Eo ’[0-9]+\_[0-9]+\.txt’ | awk -F’[_.]’ ’{print $1, $2}’ | sort -n > ../pos_id_cal.txt

Paso 2.
cd ..

Paso 3.
paste -d’ ’ <(tail -n +1 urls_pos.txt) pos_id_cal.txt | awk ’{print $1, $3}’ > url_cal_pos.txt

Paso 4.
awk ’{ puntos[$1] += $2; suma[$1]++} END { for (url in puntos) print url, puntos[url]/suma[url]}’ url_cal_pos.txt | sort -k2,2nr | head -n 10 > promedio_pos.txt


Esto mostrara el resultado en fomra de lista. De manera ilustrativa en el archivo "Solucion_linea_comando", el cual es un archivo pdf que se encuentra en el directorio cmd.

*********************************************************************************************************************

Instrucciones para resolver el problema en linea de comando (EN WINDOWS con python3.12)
---------------------------------------------------------------------------------------------------------------------

Para hacer lo propio usando python usamos diversas funciones y modulos de python los cuales se pueden consultar y revisar a detalle en la libreta llamada "Funciones" en el directorio llamada notebooks, dentro del directorio de python.
En el archivo previamente comentado estan los comentarios sobre las funciones. Los modulos y funciones se muestrab a continuacion:

import os  # modulo para interactuar con el sistema operativo
import urllib.request  # modulo para realizar solicitudes HTTP
import pandas as pd  # biblioteca para manipulacion de datos en DataFrames
import tarfile  # modulo para manejar archivos tar
from collections import defaultdict  # para crear diccionarios con valores predeterminados
from pathlib import Path  # para manejar rutas de archivos y directorios
import requests  # biblioteca para realizar solicitudes HTTP
from bs4 import BeautifulSoup  # biblioteca para extraer datos de archivos HTML y XML

1. descargar_archivo(url, directorio): '''Descarga un archivo desde la URL especificada y lo guarda en el directorio indicado. Si el archivo ya existe, no se descarga de nuevo.'''

2. descomprimir_tar_gz(archivo, directorio): '''Descomprime un archivo .tar.gz en el directorio especificado.'''

3. leer_puntuaciones(directorio): '''Lee las puntuaciones de los archivos en el directorio dado y las organiza por identificador.'''

4. calcular_promedios(puntuaciones): '''Calcula los promedios de las puntuaciones para cada identificador y devuelve un conjunto de (identificador, promedio).'''

5. obtener_top_n(promedios, n=10, mejor=True): '''Obtiene las top n películas con mejor o peor promedio. Devuelve una lista de (película, promedio) sin repeticiones.'''

6. procesar_url(url): '''Procesa una URL para eliminar la parte que incluye '/usercomments' y retorna la parte relevante.'''

7. obtener_nombre_pelicula(url): '''Obtiene el nombre de la película a partir de la url utilizando scraping. Retorna el título o un mensaje de error si no se encuentra.'''

8. crear_dataframe(peliculas, urls_path): '''Crea un DataFrame de pandas a partir de las películas y las urls. Retorna un DataFrame con la url, el nombre de la película y su promedio.'''

9. imprimir_peliculas(titulo, peliculas): '''Imprime en consola el título y la lista de películas con su promedio y URL.'''

10. analizar_peliculas(directorio_pos, directorio_neg, urls_pos, urls_neg): '''Coordina el proceso de análisis de películas, incluyendo la lectura de puntuaciones, cálculo de promedios y la impresión de resultados.'''


Tenemos una notebook llamada "Ejemplo_no_POO" el cual encuentra la solucion sin usar programacion a objetos (POO). Esta fue la manera inicial de atacar el problema.

Una vez resulto el problema sin usar POO se pudo crear una clase, la cual se comprueba su uso en una notebook llamada "Ejemplo_POO", usando el modulo creado en esta notebook.
El modulo creado lleva por nombre "IMDbprocessor" el cual esta dentro del archivo "processor" en el directorio python, esta se invoca en el "__init__" en el mismo directorio.
La manera de invocar nuestra clase es con la siguiente estructura:
from ..imdb.processor import IMDbProcessor

def main():
    url = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
    directorio = "./downloads/basedatos/aclImdb"
    directorio_pos = './downloads/basedatos/aclImdb/aclImdb/train/pos'
    directorio_neg = './downloads/basedatos/aclImdb/aclImdb/train/neg'
    urls_pos = './downloads/basedatos/aclImdb/aclImdb/train/urls_pos.txt'
    urls_neg = './downloads/basedatos/aclImdb/aclImdb/train/urls_neg.txt'

    procesador = IMDbProcessor(url, directorio, directorio_pos, directorio_neg, urls_pos, urls_neg)
    archivo = procesador.descargar_archivo()
    procesador.descomprimir_tar_gz(archivo)
    procesador.analizar_peliculas()

if __name__ == "__main__":
    main()




Adicionalmente, en el directorio de pyhton se encuentra un directorio llamado Scripts, el cual se puede ejecutar desde la terminal con el siguiente comando:

python -m python.scripts.ejecutar_analisis

Este script fue el que se uso todo el tiempo para comprobar el funcionamiento de nuestri entorno y que nuestra clase funcionara bien.











