
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

def configurar_logging():
    """
    Configura el sistema de registro.
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def save_data(data):
    """
    Guarda los datos en un archivo CSV.
    """
    df = pd.DataFrame(data)
    df.to_csv('files/archivo_de_salida.csv',encoding='utf-8')


def extract_data(lista_de_noticias):
    """
    Extrac data.
    """

    data = []

    for noticia in lista_de_noticias:

        titulo = noticia.find('span', class_='titleline').text
        url = noticia.find('span', class_='titleline').find('a').get('href')
        score = 0
        comentarios = 0
        metadata = noticia.find_next_sibling()

        try:
            score_tmp = metadata.find('span', class_='score').text
            score_tmp = score_tmp.replace('points', '').strip()
            score = int(score_tmp)
        except Exception as e:
            logging.error('No se encontro score')

        try:
            
            subline = metadata.find(attrs={'class': 'subline'}).text
            info = subline.split('|')
            comentarios_tmp = info[-1]
            comentarios_tmp = comentarios_tmp.replace('comments', '').strip()
            comentarios = int(comentarios_tmp)
        except:
            logging.error('No se encontraron comentarios')


        data.append({'titulo': titulo, 'url': url, 'score': score, 'comentarios': comentarios})

    return data

def main():
    """
    Main function.
    """
    configurar_logging()

    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    url = 'https://news.ycombinator.com/' 

    respuesta = requests.get(url, headers=headers)
    soup = BeautifulSoup(respuesta.text, 'lxml')
    lista_de_noticias = soup.find_all('tr', class_="athing")

    data = extract_data(lista_de_noticias)
    save_data(data)


if __name__ == '__main__':
    main()