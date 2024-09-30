import os 
import urllib.request
import pandas as pd
import tarfile
from collections import defaultdict
from pathlib import Path
import requests
from bs4 import BeautifulSoup

class IMDbProcessor:
    def __init__(self, url, directorio, directorio_pos, directorio_neg, urls_pos, urls_neg):
        self.url = url
        self.directorio = directorio
        self.directorio_pos = directorio_pos
        self.directorio_neg = directorio_neg
        self.urls_pos = urls_pos
        self.urls_neg = urls_neg

    def descargar_archivo(self):
        '''Descarga un archivo desde la URL especificada y lo guarda en el directorio indicado. 
        Si el archivo ya existe, no se descarga de nuevo.'''
        archivo = os.path.join(self.directorio, os.path.basename(self.url))
        os.makedirs(os.path.dirname(archivo), exist_ok=True)

        if not os.path.exists(archivo):
            urllib.request.urlretrieve(self.url, archivo)
            print(f"Descargado en {archivo}")
        else:
            print(f"El archivo ya existe.")
        return archivo

    def descomprimir_tar_gz(self, archivo):
        '''Descomprime un archivo .tar.gz en el directorio especificado.'''
        with tarfile.open(archivo, "r:gz") as tar:
            tar.extractall(path=self.directorio)
            print(f"Descomprimido en {self.directorio}.")

    def leer_puntuaciones(self, directorio):
        '''Lee las puntuaciones de los archivos en el directorio dado y las organiza por identificador.'''
        puntuaciones = defaultdict(list)
        for subdir, _, files in os.walk(directorio):
            for file_name in files:
                try:
                    identificador, puntuacion_str = file_name.split('_')
                    puntuacion = int(puntuacion_str.split('.')[0])
                    puntuaciones[identificador].append(puntuacion)
                except (ValueError, IndexError):
                    continue
        return puntuaciones

    def calcular_promedios(self, puntuaciones):
        '''Calcula los promedios de las puntuaciones para cada identificador y devuelve un conjunto de (identificador, promedio).'''
        promedios_conjunto = set()
        for identificador, scores in puntuaciones.items():
            promedio = sum(scores) / len(scores)
            promedios_conjunto.add((identificador, promedio))  # Guardamos (película, promedio) en un conjunto
        return promedios_conjunto

    def obtener_top_n(self, promedios, n=10, mejor=True):
        '''Obtiene las top N películas con mejor o peor promedio. 
        Devuelve una lista de (película, promedio) sin repeticiones.'''
        sorted_movies = sorted(promedios, key=lambda x: x[1], reverse=mejor)

        peliculas_unicas = []
        vistos = set()

        for pelicula, promedio in sorted_movies:
            if pelicula not in vistos:
                peliculas_unicas.append((pelicula, promedio))
                vistos.add(pelicula)
            if len(peliculas_unicas) == n:
                break

        return peliculas_unicas

    def procesar_url(self, url):
        '''Procesa una URL para eliminar la parte que incluye '/usercomments' y retorna la parte relevante.'''
        return url.split('/usercomments')[0]

    def obtener_nombre_pelicula(self, url):
        '''Obtiene el nombre de la película a partir de la URL utilizando web scraping. 
        Retorna el título o un mensaje de error si no se encuentra.'''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            return "Acceso denegado (403 Forbidden)"

        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.replace(' - IMDb', '').strip()
        else:
            return "Título no encontrado"

    def crear_dataframe(self, peliculas, urls_path):
        '''Crea un DataFrame de pandas a partir de las películas y las URLs. 
        Retorna un DataFrame con la url, el nombre de la película y su promedio.'''
        urls = Path(urls_path).read_text().splitlines()
        data = []
        nombres_vistos = set()

        for identificador, promedio in peliculas:
            url = self.procesar_url(urls[int(identificador) - 1])
            nombre_pelicula = self.obtener_nombre_pelicula(url)

            if nombre_pelicula not in nombres_vistos:
                nombres_vistos.add(nombre_pelicula)
                data.append({'url': url, 'Película': nombre_pelicula, 'Promedio': promedio})

        return pd.DataFrame(data)

    def imprimir_peliculas(self, titulo, peliculas):
        '''Imprime en consola el título y la lista de películas con su promedio y URL.'''
        print(titulo)
        for pelicula in peliculas:
            print(f"Película: {pelicula['Película']} || Promedio: {pelicula['Promedio']:.2f} || url: {pelicula['url']}")

    def analizar_peliculas(self):
        '''Coordina el proceso de análisis de películas, 
        incluyendo la lectura de puntuaciones, cálculo de promedios y la impresión de resultados.'''
        calificaciones_pos = self.leer_puntuaciones(self.directorio_pos)
        calificaciones_neg = self.leer_puntuaciones(self.directorio_neg)

        promedios_pos = self.calcular_promedios(calificaciones_pos)
        promedios_neg = self.calcular_promedios(calificaciones_neg)

        mejores_peliculas = self.obtener_top_n(promedios_pos, n=10)
        peores_peliculas = self.obtener_top_n(promedios_neg, n=10, mejor=False)

        lista_mejores = self.crear_dataframe(mejores_peliculas, self.urls_pos)
        lista_peores = self.crear_dataframe(peores_peliculas, self.urls_neg)

        while len(lista_mejores) < 10:
            n_a_row = pd.DataFrame({'url': [''], 'Película': ['N/A'], 'Promedio': [0]})
            lista_mejores = pd.concat([lista_mejores, n_a_row], ignore_index=True)

        while len(lista_peores) < 10:
            n_a_row = pd.DataFrame({'url': [''], 'Película': ['N/A'], 'Promedio': [0]})
            lista_peores = pd.concat([lista_peores, n_a_row], ignore_index=True)

        self.imprimir_peliculas("Las 10 películas mejor calificadas:\n", lista_mejores.to_dict(orient='records'))
        self.imprimir_peliculas("Las 10 películas peor calificadas:\n", lista_peores.to_dict(orient='records'))
