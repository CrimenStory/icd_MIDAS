import json
import pandas as pd
import matplotlib.pyplot as plt
import glob


path = 'restaurantes/*.json'  
all_files = glob.glob(path)


horas_apertura = {}
horas_cierre = {}


for filename in all_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:  
            data = json.load(f)
            
            if isinstance(data, dict):
                data = [data]  

            
            for restaurant in data:
                schedule = restaurant.get('schedule', {})
                opening_hours = set() 
                closing_hours = set()  

                for day, hours in schedule.items():
                    opening = hours.get('opening')
                    closing = hours.get('closing')
                    if opening:
                        opening_hours.add(opening)  
                    if closing:
                        closing_hours.add(closing)  

                # Horas únicas por restaurante
                for hour in opening_hours:
                    if hour in horas_apertura:
                        horas_apertura[hour] += 1
                    else:
                        horas_apertura[hour] = 1

                for hour in closing_hours:
                    if hour in horas_cierre:
                        horas_cierre[hour] += 1
                    else:
                        horas_cierre[hour] = 1

    except PermissionError:
        print(f"Permiso denegado para el archivo: {filename}")
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON: {filename}")
    except UnicodeDecodeError as e:
        print(f"Error de codificación en el archivo {filename}: {e}")
    except Exception as e:
        print(f"Error procesando el archivo {filename}: {e}")


apertura_counts = pd.Series(horas_apertura)
cierre_counts = pd.Series(horas_cierre)


print("Horas más comunes de apertura:")
print(apertura_counts.sort_values(ascending=False))


print("\nHoras más comunes de cierre:")
print(cierre_counts.sort_values(ascending=False))

# Horas más comunes
plt.figure(figsize=(12, 6))

# Horas de apertura
plt.subplot(1, 2, 1)
apertura_counts.sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue')
plt.title('Horas más comunes de apertura')
plt.xlabel('Hora de apertura')
plt.ylabel('Cantidad de restaurantes')

# Horas de cierre
plt.subplot(1, 2, 2)
cierre_counts.sort_values(ascending=False).head(10).plot(kind='bar', color='salmon')
plt.title('Horas más comunes de cierre')
plt.xlabel('Hora de cierre')
plt.ylabel('Cantidad de restaurantes')

plt.tight_layout()
plt.show()