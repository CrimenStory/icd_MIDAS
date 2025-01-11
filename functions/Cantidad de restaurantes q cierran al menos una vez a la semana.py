import json
import pandas as pd
import glob


path = 'restaurantes/*.json' 
all_files = glob.glob(path)

# Contador 
restaurantes_cerrados = 0


for filename in all_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f: 
            data = json.load(f)
            if isinstance(data, dict):
                data = [data]  

            
            for restaurant in data:
                schedule = restaurant.get('schedule', {})
                for day, hours in schedule.items():
                    closing = hours.get('closing')
                    if closing is None:  
                        restaurantes_cerrados += 1
                        break  

    except PermissionError:
        print(f"Permiso denegado para el archivo: {filename}")
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON: {filename}")
    except UnicodeDecodeError as e:
        print(f"Error de codificación en el archivo {filename}: {e}")
    except Exception as e:
        print(f"Error procesando el archivo {filename}: {e}")


print(f"Cantidad de restaurantes que cierran al menos una vez a la semana: {restaurantes_cerrados}")