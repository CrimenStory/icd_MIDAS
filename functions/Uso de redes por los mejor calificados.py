import json
import os
from collections import Counter
import matplotlib.pyplot as plt


ruta_carpeta = 'restaurantes'


def analizar_redes_sociales(ruta_carpeta):
    calificaciones = [4.5]
    redes_sociales = []
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith('.json'):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo_json:
                    data = json.load(archivo_json)
                    for calificacion in calificaciones:
                        if 'quality' in data and 'qualification_tripadvisor' in data['quality'] and data['quality']['qualification_tripadvisor'] == calificacion:
                            if 'social_networks' in data:
                                redes_sociales.extend(data['social_networks'])
            except UnicodeDecodeError:
                print(f"Error de codificación al leer el archivo: {ruta_archivo}. Intentando con 'latin-1'.")
                try:
                    with open(ruta_archivo, 'r', encoding='latin-1') as archivo_json:
                        data = json.load(archivo_json)
                        for calificacion in calificaciones:
                            if 'quality' in data and 'qualification_tripadvisor' in data['quality'] and data['quality']['qualification_tripadvisor'] == calificacion:
                                if 'social_networks' in data:
                                    redes_sociales.extend(data['social_networks'])
                except Exception as e:
                    print(f"Error al procesar el archivo {ruta_archivo}: {e}")
    contador_redes = Counter(redes_sociales)

    return contador_redes


resultado = analizar_redes_sociales(ruta_carpeta)

if resultado:
    redes = [red for red in resultado.keys() if red is not None]
    conteos = [resultado[red] for red in redes]
    plt.figure(figsize=(10, 6))
    plt.bar(redes, conteos, color='skyblue')
    plt.xlabel('Redes Sociales')
    plt.ylabel('Número de Usos')
    plt.title('Uso de Redes Sociales por Mejores Calificados (4.5)')
    plt.xticks(rotation=45)
    plt.tight_layout() 
    plt.show()
else:
    print("No se encontraron redes sociales para los mejores calificados.")