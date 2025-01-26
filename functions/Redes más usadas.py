import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter


folder_path = 'restaurantes'  

social_networks_list = []


for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if 'social_networks' in data:
            valid_networks = [network for network in data['social_networks'] if network is not None]
            social_networks_list.extend(valid_networks)


social_networks_count = Counter(social_networks_list)


df_social_networks = pd.DataFrame(social_networks_count.items(), columns=['Platform', 'Count'])


df_social_networks = df_social_networks.sort_values(by='Count', ascending=False)


print("Plataformas de Redes Sociales Más Usadas:")
print(df_social_networks)

plt.figure(figsize=(10, 6))
plt.bar(df_social_networks['Platform'], df_social_networks['Count'], color='skyblue')
plt.title('Plataformas de Redes Sociales Más Usadas por Restaurantes', fontsize=16)
plt.xlabel('Plataforma', fontsize=14)
plt.ylabel('Número de Restaurantes', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()