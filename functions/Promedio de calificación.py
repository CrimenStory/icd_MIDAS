import os
import json
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def cargar_datos_json(carpeta):
    datos = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.json'):
            with open(os.path.join(carpeta, archivo), 'r', encoding='utf-8') as f:
                try:
                    datos.append(json.load(f))
                except json.JSONDecodeError:
                    print(f"Error al decodificar el archivo {archivo}")
    return datos

def calcular_calificaciones_por_municipio(data, min_restaurantes=5):
    calificaciones_por_municipio = defaultdict(list)

    for registro in data:
        if "locality" in registro and "quality" in registro:
            municipio = registro["locality"]["mun"]
            google_calif = registro["quality"].get("qualification_google")
            tripadvisor_calif = registro["quality"].get("qualification_tripadvisor")
            facebook_calif = registro["quality"].get("qualification_facebook")

            # Agregar calificaciones válidas
            if google_calif is not None:
                calificaciones_por_municipio[municipio].append(google_calif)
            if tripadvisor_calif is not None:
                calificaciones_por_municipio[municipio].append(tripadvisor_calif)
            if facebook_calif is not None:
                calificaciones_por_municipio[municipio].append(facebook_calif)

    # Filtrar municipios con suficientes restaurantes y calcular promedios
    promedios_por_municipio = {
        mun: np.mean(calif) 
        for mun, calif in calificaciones_por_municipio.items() 
        if len(calif) >= min_restaurantes
    }
    
    return promedios_por_municipio

def graficar_calificaciones_por_municipio(promedios):
    # Ordenar municipios por calificación promedio
    municipios_ordenados = sorted(promedios.items(), key=lambda x: x[1], reverse=True)
    municipios, calificaciones = zip(*municipios_ordenados)

    plt.figure(figsize=(12, 6))
    plt.bar(municipios, calificaciones, color='skyblue')
    plt.xlabel('Municipios')
    plt.ylabel('Calificación Promedio')
    plt.title('Calificaciones Promedio por Municipio (mínimo de restaurantes)')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 5)  # Asumiendo que las calificaciones son de 0 a 5
    plt.tight_layout()
    plt.show()


carpeta_json = 'restaurantes'

# Cargar datos
datos = cargar_datos_json(carpeta_json)

# Calcular calificaciones por municipio
promedios = calcular_calificaciones_por_municipio(datos, min_restaurantes=5)

# Graficar calificaciones por municipio
graficar_calificaciones_por_municipio(promedios)