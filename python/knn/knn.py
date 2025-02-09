import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import roc_curve, auc
from sklearn.feature_extraction.text import TfidfVectorizer

# Caricamento dataset
df = pd.read_csv("csv/final_dataset.csv")

# Conversione 'tof' in numerico (Fake=0, True=1)
df['tof_numeric'] = df['tof'].map({'Fake': 0, 'True': 1})

# One-Hot Encoding per 'subject'
subject_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
subject_encoded = subject_encoder.fit_transform(df[['subject']])
subject_df = pd.DataFrame(subject_encoded, columns=subject_encoder.get_feature_names_out(['subject']))

# Unione delle feature numeriche e one-hot
X_other = df[['num_words', 'suspicious_political_news', 'suspicious_clickbait_news']]
X = pd.concat([X_other, subject_df], axis=1)
y = df['tof_numeric']

# Estrazione delle feature dal testo
text_data = df['text']

# Creazione della matrice TF-IDF dal testo
tfidf_vectorizer = TfidfVectorizer(max_features=400)
X_text = tfidf_vectorizer.fit_transform(text_data).toarray()  # Crea la matrice TF-IDF

# Unione della matrice TF-IDF alle feature numeriche e alla feature subject codificata con one-hot encoding
X = np.hstack((X, X_text))  # Uniamo numeriche + testo

# Suddivisione dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalizzazione
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Addestramento modello K-NN
knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(X_train, y_train)


print("\nValutazione del modello KNN sul test set con calcolo e stampa della curva di ROC e dell'AUC")

# predidizioni    
y_pred = knn.predict(X_test)

# Calcolo dell'accuratezza
accuracy = accuracy_score(y_test, y_pred)

# Stampa dell'accuratezza
print(f"Accuratezza del modello: {accuracy:.4f}")

# Predizioni probabilistiche (per ottenere la probabilità per la classe positiva "True")
y_prob = knn.predict_proba(X_test)[:,1]

# Calcolo della curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_prob)

# Calcolo e stampa dell'AUC (Area sotto la curva di ROC)
roc_auc = auc(fpr, tpr)
print(f'Area sotto la curva ROC (AUC): {roc_auc:.4f}')

# Tracciamento della curva ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', label=f'Curva ROC (AUC = {roc_auc:.4f})')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Tasso di Falsi Positivi (FPR)')
plt.ylabel('Tasso di Veri Positivi (TPR)')
plt.title('Curva ROC per il Modello K-NN\n(chiudire la finestra per continuare)')
plt.legend(loc="lower right")
plt.show()


print("\nValutazione del modello KNN con 5-fold cross validation")

# Valutazione del modello con k-fold cross-validation
print("Esecuzione k-fold cross-validation...")

# Esegui la k-fold cross-validation sul modello KNN
accuracies = cross_val_score(knn, X, y, cv=5, scoring='accuracy')

# Calcolo dell'accuratezza media e della deviazione standard
accuracy_mean = accuracies.mean()
accuracy_std = accuracies.std()

# Stampa dell'accuratezza media e della deviazione standard
print(f"Accuratezza media con {5}-Fold Cross-Validation: {accuracy_mean:.4f}")
print(f"Deviazione standard dell'accuratezza: {accuracy_std:.4f}")