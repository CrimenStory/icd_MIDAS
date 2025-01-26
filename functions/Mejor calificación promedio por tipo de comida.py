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

                 
                    scores = [
                        qualifications_data.get('qualification_google'),
                        qualifications_data.get('qualification_tripadvisor'),
                        qualifications_data.get('qualification_facebook')
                    ]

                    scores = [score for score in scores if score is not None]
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


ruta = 'restaurantes'  

qualifications = analyze_json_files(ruta)

average_qualifications = {
    cuisine: (sum(scores) / len(scores)) if scores else 0
    for cuisine, scores in qualifications.items()
}

sorted_cuisines = sorted(average_qualifications, key=average_qualifications.get, reverse=True)

scores = [average_qualifications[cuisine] for cuisine in sorted_cuisines]

plt.figure(figsize=(10, 6))
plt.barh(sorted_cuisines, scores, color='skyblue')
plt.xlabel('Calificación Promedio')
plt.title('Mejor Calificación Promedio por Tipo de Comida')
plt.grid(axis='x')

plt.show()