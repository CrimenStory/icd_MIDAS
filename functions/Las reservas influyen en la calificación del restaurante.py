import os
import json
import pandas as pd
import matplotlib.pyplot as plt


folder_path = 'restaurantes'  


with_reservation = []
without_reservation = []


for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                restaurant = json.load(file)
                
                
                qualifications = [
                    restaurant['quality'].get('qualification_google'),
                    restaurant['quality'].get('qualification_tripadvisor'),
                    restaurant['quality'].get('qualification_facebook')
                ]
                
                
                qualifications = [q for q in qualifications if q is not None]
                
                
                if qualifications:
                    avg_qualification = sum(qualifications) / len(qualifications)
                    
                    if restaurant['reservation_options']:
                        with_reservation.append(avg_qualification)
                    else:
                        without_reservation.append(avg_qualification)
            except json.JSONDecodeError:
                print(f"Error al decodificar el archivo JSON: {file_path}")
            except Exception as e:
                print(f"Error al procesar el archivo {file_path}: {e}")

# Calcula promedios
avg_with_reservation = sum(with_reservation) / len(with_reservation) if with_reservation else 0
avg_without_reservation = sum(without_reservation) / len(without_reservation) if without_reservation else 0

# Gráfico de comparación
labels = ['Con Reserva', 'Sin Reserva']
averages = [avg_with_reservation, avg_without_reservation]

plt.figure(figsize=(8, 5))
plt.bar(labels, averages, color=['blue', 'orange'])


plt.ylabel('Calificación Promedio')
plt.title('Comparación de Calificaciones Promedio de Restaurantes')
plt.ylim(0, 5)  


plt.tight_layout()  
plt.show()


print(f"Calificación promedio de restaurantes con reserva: {avg_with_reservation:.2f}")
print(f"Calificación promedio de restaurantes sin reserva: {avg_without_reservation:.2f}")