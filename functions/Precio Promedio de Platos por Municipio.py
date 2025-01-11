import json
import pandas as pd
import plotly.express as px
import os


folder_path = 'restaurantes'  


data_list = []


for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

       
        municipality = data['locality']['mun']

        
        if 'menu' in data:
            # Extraer precios de los platos principales
            if 'main_courses' in data['menu']:
                for dish in data['menu']['main_courses']:
                    if dish and 'item' in dish and 'price' in dish:
                        price = dish['price']
                        # Asegurarse de que el precio sea numérico
                        if isinstance(price, (int, float)):
                            data_list.append({'municipality': municipality, 'price': price})

# Crear un DataFrame
df = pd.DataFrame(data_list)

# Agrupar por municipio y calcular el precio promedio
average_price_by_municipality = df.groupby('municipality')['price'].mean().reset_index()

# Función para eliminar outliers usando el método IQR
def remove_outliers(data):
    Q1 = data['price'].quantile(0.25)
    Q3 = data['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data['price'] >= lower_bound) & (data['price'] <= upper_bound)]

# Eliminar outliers
df_cleaned = remove_outliers(df)

# Recalcula el precio promedio después de eliminar outliers
average_price_by_municipality_cleaned = df_cleaned.groupby('municipality')['price'].mean().reset_index()

# Redondea los precios a números naturales
average_price_by_municipality_cleaned['price'] = average_price_by_municipality_cleaned['price'].round().astype(int)

# Imprimir los precios promedio por municipio
print("Precios Promedio de Platos Principales por Municipio:")
print(average_price_by_municipality_cleaned)

# Crear un gráfico interactivo para visualizar los precios promedio por municipio
fig = px.bar(average_price_by_municipality_cleaned, x='municipality', y='price',
             title='Precio Promedio de Platos Principales por Municipio',
             labels={'price': 'Precio Promedio', 'municipality': 'Municipio'},
             text='price')

# Mostrar el gráfico
fig.show()