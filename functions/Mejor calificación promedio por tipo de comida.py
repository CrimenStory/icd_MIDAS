import json
import os
import matplotlib.pyplot as plt

def analyze_json_files(directory):
    qualifications = {}

    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)

                    
                    type_cuisine_list = data['type_cuisine']
                    qualifications_data = data['quality']

                    # Extrae las calificaciones individuales, ignorando None
                    scores = [
                        qualifications_data.get('qualification_google'),
                        qualifications_data.get('qualification_tripadvisor'),
                        qualifications_data.get('qualification_facebook')
                    ]

                    # Filtrar calificaciones válidas 
                    scores = [score for score in scores if score is not None]

                    # Almacenar las calificaciones por tipo de comida
                    for type_cuisine in type_cuisine_list:
                        if type_cuisine in qualifications:
                            qualifications[type_cuisine].extend(scores)
                        else:
                            qualifications[type_cuisine] = scores.copy()

                except json.JSONDecodeError:
                    print(f"Error al decodificar el archivo {filename}.")
                except KeyError as e:
                    print(f"Falta la clave {e} en el archivo {filename}.")

    return qualifications


directory_path = 'restaurantes'  

# Llamar a la función y obtener el resultado
qualifications = analyze_json_files(directory_path)

# Calcular la mejor calificación promedio por tipo de comida
average_qualifications = {
    cuisine: (sum(scores) / len(scores)) if scores else 0
    for cuisine, scores in qualifications.items()
}

# Ordenar los tipos de comida por calificación promedio
sorted_cuisines = sorted(average_qualifications, key=average_qualifications.get, reverse=True)

# Preparar datos para el gráfico
scores = [average_qualifications[cuisine] for cuisine in sorted_cuisines]

# Crear gráfico de barras
plt.figure(figsize=(10, 6))
plt.barh(sorted_cuisines, scores, color='skyblue')
plt.xlabel('Calificación Promedio')
plt.title('Mejor Calificación Promedio por Tipo de Comida')
plt.grid(axis='x')

# Mostrar gráfico
plt.show()