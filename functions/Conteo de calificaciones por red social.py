import os
import json
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

def contar_calificaciones(data):
    conteo_calificaciones = {
        "Google": 0,
        "TripAdvisor": 0,
        "Facebook": 0
    }

    for registro in data:
        if "quality" in registro:
            google_calif = registro["quality"].get("qualification_google")
            tripadvisor_calif = registro["quality"].get("qualification_tripadvisor")
            facebook_calif = registro["quality"].get("qualification_facebook")

            # Contar solo si la calificación no es None
            if google_calif is not None:
                conteo_calificaciones["Google"] += 1
            if tripadvisor_calif is not None:
                conteo_calificaciones["TripAdvisor"] += 1
            if facebook_calif is not None:
                conteo_calificaciones["Facebook"] += 1

    return conteo_calificaciones

def graficar_grafico_barras_horizontal(resultados):
    redes_sociales = list(resultados.keys())
    conteos = [resultados[red] for red in redes_sociales]

    plt.figure(figsize=(8, 6))
    plt.barh(redes_sociales, conteos, color=['orange', 'green', 'blue'])
    plt.xlabel('Número de Calificaciones Válidas')
    plt.ylabel('Redes Sociales')
    plt.title('Conteo de Calificaciones Válidas por Red Social')
    plt.tight_layout()
    plt.show()


carpeta_json = 'restaurantes'

# Cargar datos
datos = cargar_datos_json(carpeta_json)

# Contar calificaciones
resultados = contar_calificaciones(datos)

graficar_grafico_barras_horizontal(resultados)