import os
import json
from collections import Counter
import matplotlib.pyplot as plt


folder_path = 'restaurantes'  


phone_types = []


for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        

        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                restaurant = json.load(file)
                

                landline = restaurant['locality']['locator']['phones']['landline']
                mobile = restaurant['locality']['locator']['phones']['mobile']
                

                if landline and mobile:
                    phone_types.append('Ambos')
                elif landline:
                    phone_types.append('Fijo')
                elif mobile:
                    phone_types.append('Móvil')
                else:
                    phone_types.append('Ninguno')  
            except json.JSONDecodeError:
                print(f"Error al decodificar el archivo JSON: {file_path}")
            except Exception as e:
                print(f"Error al procesar el archivo {file_path}: {e}")


phone_count = Counter(phone_types)


print("Análisis de tipos de teléfono en restaurantes:")
for phone_type, count in phone_count.items():
    print(f"{phone_type}: {count} restaurantes")


labels = phone_count.keys()
sizes = phone_count.values()
colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']  

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  
plt.title('Distribución de Tipos de Teléfono en Restaurantes')
plt.show()