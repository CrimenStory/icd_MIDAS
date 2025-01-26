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

            if 'main_courses' in data['menu']:
                for dish in data['menu']['main_courses']:
                    if dish and 'item' in dish and 'price' in dish:
                        price = dish['price']

                        if isinstance(price, (int, float)):
                            data_list.append({'municipality': municipality, 'price': price})

df = pd.DataFrame(data_list)


average_price_by_municipality = df.groupby('municipality')['price'].mean().reset_index()

def quita_cosas_raras(data):
    Q1 = data['price'].quantile(0.25)
    Q3 = data['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data['price'] >= lower_bound) & (data['price'] <= upper_bound)]

df_cleaned = quita_cosas_raras(df)

average_price_by_municipality_cleaned = df_cleaned.groupby('municipality')['price'].mean().reset_index()

average_price_by_municipality_cleaned['price'] = average_price_by_municipality_cleaned['price'].round().astype(int)

print("Precios Promedio de Platos Principales por Municipio:")
print(average_price_by_municipality_cleaned)

fig = px.bar(average_price_by_municipality_cleaned, x='municipality', y='price',
             title='Precio Promedio de Platos Principales por Municipio',
             labels={'price': 'Precio Promedio', 'municipality': 'Municipio'},
             text='price')

fig.show()