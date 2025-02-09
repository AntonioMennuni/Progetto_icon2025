import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Carica il dataset (esempio: df_encoded)
input_file = 'csv/clean_dataset_with_num_words.csv'
df = pd.read_csv(input_file, encoding='ISO-8859-1', header=0)

# Applica One-Hot Encoding alla colonna 'subject'
df_encoded = pd.get_dummies(df, columns=['subject'])

# Seleziona le feature numeriche per il clustering
X = df_encoded[['num_words'] + [col for col in df_encoded.columns if 'subject_' in col]]

# Lista per memorizzare i valori dell'inertia (somma delle distanze quadratiche)
inertia_values = []

# Prova diversi valori di k (ad esempio da 1 a 10)
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia_values.append(kmeans.inertia_)

# Plot della curva dell'elbow
plt.plot(range(1, 11), inertia_values, marker='o', linestyle='--')
plt.title('Metodo dell\'Elbow')
plt.xlabel('Numero di cluster (k)')
plt.ylabel('Inertia (SSE)')
plt.show()