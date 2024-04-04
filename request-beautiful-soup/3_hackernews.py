import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

def configurar_logging():
    """
    Configura el sistema de registro.
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def obtener_lista_de_noticias(url, headers):
    """
    Obtiene la lista de noticias de la página web.
    """
    respuesta = requests.get(url, headers=headers)
    soup = BeautifulSoup(respuesta.text, 'lxml')
    return soup.find_all('tr', class_="athing")

def extraer_datos_de_noticia(noticia):
    """
    Extrae los datos relevantes de una noticia.
    """
    titulo_elemento = noticia.find('span', class_='storylink')
    titulo = titulo_elemento.text if titulo_elemento else "No se encontró título"
    url_elemento = noticia.find('a', class_='storylink')
    url = url_elemento['href'] if url_elemento else "No se encontró URL"

    metadata = noticia.find_next_sibling()
    score = 0
    comentarios = 0

    try:
        score_elemento = metadata.find('span', class_='score')
        score = int(score_elemento.text.split()[0]) if score_elemento else 0
    except Exception as e:
        logging.error(f"Error al obtener score: {e}")

    try:
        comentarios_elemento = metadata.find('a', string=lambda text: 'comment' in text.lower())
        comentarios = int(comentarios_elemento.text.split()[0]) if comentarios_elemento else 0
    except Exception as e:
        logging.error(f"Error al obtener comentarios: {e}")

    return [titulo, url, score, comentarios]

def procesar_noticias(lista_de_noticias):
    """
    Procesa la lista de noticias y devuelve una lista de datos.
    """
    return [extraer_datos_de_noticia(noticia) for noticia in lista_de_noticias]

def guardar_datos(data, filename):
    """
    Guarda los datos en un archivo CSV.
    """
    df = pd.DataFrame(data, columns=['Título', 'URL', 'Score', 'Comentarios'])
    df.to_csv(filename, index=False, encoding='utf-8')

def main():
    """
    Función principal que orquesta el proceso.
    """
    configurar_logging()
    
    url = 'https://news.ycombinator.com/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    lista_de_noticias = obtener_lista_de_noticias(url, headers)
    if lista_de_noticias:
        data = procesar_noticias(lista_de_noticias)
        guardar_datos(data, 'archivo_de_salida.csv')
        logging.info("Proceso completado.")
    else:
        logging.error("No se pudo obtener la lista de noticias.")

if __name__ == "__main__":
    main()
