import os
import json
from collections import Counter
import matplotlib.pyplot as plt


folder_path = 'restaurantes'  


phone_types = []


for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        # Cargar los datos JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                restaurant = json.load(file)
                
                # Obtener los números de teléfono
                landline = restaurant['locality']['locator']['phones']['landline']
                mobile = restaurant['locality']['locator']['phones']['mobile']
                
                # Determinar el tipo de teléfono
                if landline and mobile:
                    phone_types.append('Ambos')
                elif landline:
                    phone_types.append('Fijo')
                elif mobile:
                    phone_types.append('Móvil')
                else:
                    phone_types.append('Ninguno')  # Si no hay ninguno

            except json.JSONDecodeError:
                print(f"Error al decodificar el archivo JSON: {file_path}")
            except Exception as e:
                print(f"Error al procesar el archivo {file_path}: {e}")

# Contar la frecuencia de cada tipo de teléfono
phone_count = Counter(phone_types)

# Mostrar los resultados
print("Análisis de tipos de teléfono en restaurantes:")
for phone_type, count in phone_count.items():
    print(f"{phone_type}: {count} restaurantes")

# Crea un gráfico de pastel
labels = phone_count.keys()
sizes = phone_count.values()
colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']  # Colores para el gráfico

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Para que el gráfico sea un círculo
plt.title('Distribución de Tipos de Teléfono en Restaurantes')
plt.show()