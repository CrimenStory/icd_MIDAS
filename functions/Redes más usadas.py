import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter


folder_path = 'restaurantes'  

# Lista para almacenar redes sociales
social_networks_list = []


for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Verifica si 'social_networks' está en el JSON
        if 'social_networks' in data:
            # Filtrar plataformas que no sean None
            valid_networks = [network for network in data['social_networks'] if network is not None]
            social_networks_list.extend(valid_networks)

# Contar las plataformas de redes sociales
social_networks_count = Counter(social_networks_list)

# Crear un DataFrame 
df_social_networks = pd.DataFrame(social_networks_count.items(), columns=['Platform', 'Count'])

# Ordena el DataFrame por el número de usos
df_social_networks = df_social_networks.sort_values(by='Count', ascending=False)

# Imprimir el DataFrame
print("Plataformas de Redes Sociales Más Usadas:")
print(df_social_networks)

# Crear un gráfico de barras para visualizar las plataformas más utilizadas
plt.figure(figsize=(10, 6))
plt.bar(df_social_networks['Platform'], df_social_networks['Count'], color='skyblue')
plt.title('Plataformas de Redes Sociales Más Usadas por Restaurantes', fontsize=16)
plt.xlabel('Plataforma', fontsize=14)
plt.ylabel('Número de Restaurantes', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar el gráfico
plt.tight_layout()
plt.show()