import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Carica il dataset
input_file = 'csv/clean_dataset_with_num_words.csv'
df = pd.read_csv(input_file, encoding='ISO-8859-1', header=0)

# Applica One-Hot Encoding alla colonna 'subject'
df_encoded = pd.get_dummies(df, columns=['subject'])

# Seleziona le feature numeriche per il clustering
X = df_encoded[['num_words'] + [col for col in df_encoded.columns if 'subject_' in col]]

# Inizializza il modello K-Means
kmeans = KMeans(n_clusters=5, random_state=42)

# Fitta il modello sui dati e aggiunge il cluster al dataframe
df_encoded['cluster'] = kmeans.fit_predict(X)

# Impostiamo il formato per la stampa dei numeri (2 decimali)
np.set_printoptions(precision=2, suppress=True)

# Ottieni i nomi delle feature usate nel clustering
feature_names = ['num_words'] + [col for col in df_encoded.columns if 'subject_' in col]

# Mostra i centroidi con le feature corrispondenti
for i, centroide in enumerate(kmeans.cluster_centers_):
    print(f'\n Cluster {i}:')
    for feature, value in zip(feature_names, centroide):
        print(f'  {feature}: {value:.2f}')

# Conta il numero di elementi per ciascun cluster
cluster_counts = df_encoded['cluster'].value_counts().sort_index()

# Stampa il numero di elementi per ciascun cluster
print("\nNumero di elementi per ciascun cluster:")
for cluster, count in cluster_counts.items():
    print(f'Cluster {cluster}: {count} elementi')

# Raggruppa per 'cluster' e calcola la percentuale di notizie vere e false
cluster_stats = df_encoded.groupby(['cluster', 'tof']).size().unstack(fill_value=0)

# Calcola la percentuale di notizie vere e false per ciascun cluster
cluster_stats_percentage = cluster_stats.div(cluster_stats.sum(axis=1), axis=0) * 100

# Stampa le percentuali
print("Percentuali di notizie vere e false per ciascun cluster:")
print(cluster_stats_percentage)

# Applica PCA per ridurre a 2 dimensioni
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)  # X è il dataset con num_words e One-Hot Encoding di subject

# Crea il grafico scatter con i cluster
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df_encoded['cluster'], cmap='viridis', alpha=0.5)
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.title('Clustering K-Means con PCA')
plt.colorbar(label='Cluster')
plt.show()