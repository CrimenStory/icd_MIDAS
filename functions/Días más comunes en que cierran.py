import json
import pandas as pd
import glob
import matplotlib.pyplot as plt


path = 'restaurantes/*.json'  
all_files = glob.glob(path)

# Crear un diccionario para contar los días cerrados
dias_cerrados = {}

# Días de inglés a español
dias_traducidos = {
    "monday": "Lunes",
    "tuesday": "Martes",
    "wednesday": "Miércoles",
    "thursday": "Jueves",
    "friday": "Viernes",
    "saturday": "Sábado",
    "sunday": "Domingo"
}

# Leer cada archivo JSON y agregar los datos a una lista
for filename in all_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:  
            data = json.load(f)
            
            if isinstance(data, dict):
                data = [data]  

            # Extraer días cerrados
            for restaurant in data:
                schedule = restaurant.get('schedule', {})
                
                for day, hours in schedule.items():
                    closing = hours.get('closing')
                    if closing is None:  # Si el horario de cierre es null
                        if day in dias_cerrados:
                            dias_cerrados[day] += 1
                        else:
                            dias_cerrados[day] = 1

    except PermissionError:
        print(f"Permiso denegado para el archivo: {filename}")
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON: {filename}")
    except UnicodeDecodeError as e:
        print(f"Error de codificación en el archivo {filename}: {e}")
    except Exception as e:
        print(f"Error procesando el archivo {filename}: {e}")

# Convertir el diccionario a un DataFrame 
dias_cerrados_df = pd.Series(dias_cerrados).sort_values(ascending=False)

# Traducir los días al español
dias_cerrados_df.index = dias_cerrados_df.index.map(dias_traducidos)

# Mostrar los días más comunes en los que los restaurantes están cerrados
print("Días más comunes en los que los restaurantes están cerrados:")
print(dias_cerrados_df)

# Graficar los días más comunes
dias_cerrados_df.plot(kind='bar', color='salmon', figsize=(10, 6))
plt.title('Días más comunes en que los restaurantes permanecen cerrados')
plt.xlabel('Día de la semana')
plt.ylabel('Cantidad de restaurantes')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()