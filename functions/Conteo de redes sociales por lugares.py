import json
import os
from collections import Counter
import matplotlib.pyplot as plt


ruta_carpeta = 'restaurantes'


def contar_redes_sociales(ruta_carpeta):
    # Contador 
    conteo_redes = Counter()

    
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith('.json'):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo_json:
                    data = json.load(archivo_json)
                    if 'social_networks' in data:
                        redes = data['social_networks']
                        cantidad_redes = len(redes) if redes else 0
                        conteo_redes[cantidad_redes] += 1
            except UnicodeDecodeError:
                print(f"Error de codificación al leer el archivo: {ruta_archivo}. Intentando con 'latin-1'.")
                try:
                    with open(ruta_archivo, 'r', encoding='latin-1') as archivo_json:
                        data = json.load(archivo_json)
                        if 'social_networks' in data:
                            redes = data['social_networks']
                            cantidad_redes = len(redes) if redes else 0
                            conteo_redes[cantidad_redes] += 1
                except Exception as e:
                    print(f"Error al procesar el archivo {ruta_archivo}: {e}")
    return conteo_redes

resultado = contar_redes_sociales(ruta_carpeta)

if resultado:
    
    categorias = [0, 1, 2, 3, 4]
    conteos = [resultado.get(cat, 0) for cat in categorias]
    
    plt.figure(figsize=(10, 6))
    plt.bar(categorias, conteos, color='skyblue')
    plt.xlabel('Cantidad de Redes Sociales Usadas')
    plt.ylabel('Número de Lugares')
    plt.title('Distribución del Uso de Redes Sociales entre los Establecimientos')
    plt.xticks(categorias)
    plt.tight_layout() 
    plt.show()
else:
    print("No se encontraron datos para graficar.")