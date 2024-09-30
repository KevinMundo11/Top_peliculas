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
