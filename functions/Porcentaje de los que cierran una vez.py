import json
import pandas as pd
import glob
import matplotlib.pyplot as plt


path = 'restaurantes/*.json'  
all_files = glob.glob(path)

# Contador de restaurantes que cierran al menos una vez a la semana
restaurantes_cerrados = 0
total_restaurantes = 0


for filename in all_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:  
            data = json.load(f)
            
            if isinstance(data, dict):
                data = [data]  

            total_restaurantes += len(data)  

            # Verifica si el restaurante cierra al menos un día
            for restaurant in data:
                schedule = restaurant.get('schedule', {})
                for day, hours in schedule.items():
                    closing = hours.get('closing')
                    if closing is None:  # Si el horario de cierre es null
                        restaurantes_cerrados += 1
                        break  # Salir del bucle si ya se encontró un día cerrado

    except PermissionError:
        print(f"Permiso denegado para el archivo: {filename}")
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON: {filename}")
    except UnicodeDecodeError as e:
        print(f"Error de codificación en el archivo {filename}: {e}")
    except Exception as e:
        print(f"Error procesando el archivo {filename}: {e}")

# Calcular el porcentaje de restaurantes que cierran al menos una vez a la semana
porcentaje_cerrados = (restaurantes_cerrados / total_restaurantes) * 100 if total_restaurantes > 0 else 0
porcentaje_abiertos = 100 - porcentaje_cerrados

# Datos para el gráfico circular
labels = ['Cerrados al menos una vez a la semana', 'Abiertos toda la semana']
sizes = [porcentaje_cerrados, porcentaje_abiertos]
colors = ['salmon', 'lightblue']
explode = (0.1, 0)  

# Crear el gráfico circular
plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Porcentaje de Restaurantes que Cierran al Menos una Vez a la Semana')
plt.show()

# Mostrar resultados
print(f"Cantidad de restaurantes que cierran al menos una vez a la semana: {restaurantes_cerrados}")
print(f"Total de restaurantes analizados: {total_restaurantes}")
print(f"Porcentaje de restaurantes que cierran al menos una vez a la semana: {porcentaje_cerrados:.2f}%")