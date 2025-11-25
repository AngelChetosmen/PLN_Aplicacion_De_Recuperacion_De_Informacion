import os
import csv
import requests
from bs4 import BeautifulSoup

# Función para descargar líricas automáticamente de muchos artistas
def descargar_liricas_automaticamente():
    # Fuente base (azlyrics.com)
    base_url = "https://www.azlyrics.com/"
    
    corpus = []

    # Obtener listado de artistas desde la página principal de AZLyrics
    print("Obteniendo lista de artistas...")
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"Error al acceder a {base_url}. Código de estado: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Encontrar enlaces de artistas (organizados alfabéticamente)
        letras_secciones = soup.find_all("div", class_="container main-page")[0].find_all("a", href=True)
        artistas_enlaces = [base_url + enlace["href"].lstrip("/") for enlace in letras_secciones if enlace["href"].startswith("/")]

        print(f"Se encontraron {len(artistas_enlaces)} artistas.")
    except Exception as e:
        print(f"Error al obtener la lista de artistas: {e}")
        return
    
    # Limitar el número de artistas (por ejemplo, procesar 100 artistas para evitar tiempos excesivos)
    limite_artistas = 100
    artistas_enlaces = artistas_enlaces[:limite_artistas]
    
    # Procesar cada artista para descargar sus canciones
    for i, enlace_artista in enumerate(artistas_enlaces):
        print(f"[{i+1}/{len(artistas_enlaces)}] Procesando artista en {enlace_artista}")
        try:
            artista_response = requests.get(enlace_artista)
            if artista_response.status_code != 200:
                print(f"Error al descargar desde {enlace_artista}. Código de estado: {artista_response.status_code}")
                continue
            
            artista_soup = BeautifulSoup(artista_response.text, "html.parser")
            # Extraer enlaces de canciones
            canciones = artista_soup.find_all("a", href=True)
            canciones_enlaces = [
                base_url + enlace["href"].lstrip("/") for enlace in canciones if enlace["href"].startswith("../lyrics")
            ]
            
            for enlace_cancion in canciones_enlaces:
                try:
                    cancion_response = requests.get(enlace_cancion)
                    if cancion_response.status_code != 200:
                        print(f"Error al descargar la canción desde {enlace_cancion}. Código de estado: {cancion_response.status_code}")
                        continue
                    
                    cancion_soup = BeautifulSoup(cancion_response.text, "html.parser")
                    
                    # Extraer el título de la canción
                    titulo = cancion_soup.find("b").text.strip() if cancion_soup.find("b") else "Título desconocido"
                    
                    # Extraer la lírica
                    lirica_div = cancion_soup.find("div", class_=False, id=False)
                    lirica = lirica_div.text.strip() if lirica_div else "Lírica no encontrada"
                    
                    # Extraer el autor (nombre del artista)
                    autor = enlace_artista.split("/")[-1].capitalize() if enlace_artista.split("/")[-1] else "Autor desconocido"
                    
                    # Guardar los datos en el corpus
                    corpus.append({
                        "titulo": titulo,
                        "autor": autor,
                        "genero": "Desconocido",  # El género no está disponible directamente en AZLyrics
                        "lirica": lirica,
                        "año": "Desconocido",    # El año no está disponible directamente en AZLyrics
                        "url": enlace_cancion
                    })
                    print(f"Descargada: {titulo} por {autor}")
                except Exception as e:
                    print(f"Error procesando la canción en {enlace_cancion}: {e}")
        except Exception as e:
            print(f"Error procesando el artista en {enlace_artista}: {e}")
    
    # Guardar el corpus en un archivo CSV
    if corpus:
        nombre_archivo = "corpus_liricas.csv"
        with open(nombre_archivo, mode="w", encoding="utf-8", newline="") as archivo_csv:
            campos = ["titulo", "autor", "genero", "lirica", "año", "url"]
            escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(corpus)
        
        print(f"Corpus de líricas guardado en {nombre_archivo}")
    else:
        print("No se encontraron líricas para guardar.")

# Ejecutar el script
if __name__ == "__main__":
    descargar_liricas_automaticamente()
