import os
import json
import numpy as np
import matplotlib.pyplot as plt

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

def obtener_calificaciones(data):
    calificaciones = {
        "Google": [],
        "TripAdvisor": [],
        "Facebook": []
    }

    for registro in data:
        if "quality" in registro:
            google_calif = registro["quality"].get("qualification_google")
            tripadvisor_calif = registro["quality"].get("qualification_tripadvisor")
            facebook_calif = registro["quality"].get("qualification_facebook")

            if google_calif is not None:
                calificaciones["Google"].append(google_calif)
            if tripadvisor_calif is not None:
                calificaciones["TripAdvisor"].append(tripadvisor_calif)
            if facebook_calif is not None:
                calificaciones["Facebook"].append(facebook_calif)

    return calificaciones

def graficar_boxplot(calificaciones):
    plt.figure(figsize=(10, 6))
    plt.boxplot(calificaciones.values(), labels=calificaciones.keys())
    plt.title('Distribución de Calificaciones por Red Social')
    plt.ylabel('Calificaciones')
    plt.xlabel('Redes Sociales')
    plt.ylim(0, 5)  
    plt.grid(axis='y')
    plt.show()


carpeta_json = 'restaurantes'

datos = cargar_datos_json(carpeta_json)

calificaciones = obtener_calificaciones(datos)

graficar_boxplot(calificaciones)