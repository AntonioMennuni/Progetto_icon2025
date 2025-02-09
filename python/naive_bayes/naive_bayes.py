from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, roc_curve, auc
import pandas as pd
import matplotlib.pyplot as plt

# Caricamento del dataset
file_path = "csv/clean_dataset_with_num_words.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1', header=0)

# Separazione dei dati in input (X) e target (y)
X = df['text']  # Colonna con i testi delle notizie
y = df['tof'].map({'Fake': 0, 'True': 1})  # Conversione in valori numerici (Fake=0, True=1)

# Creazione del CountVectorizer per il Bag-of-Words
vectorizer = CountVectorizer()
X_counts = vectorizer.fit_transform(X)

# Creazione del modello Naive Bayes
nb = MultinomialNB()

# Suddivisione in training e test set
X_train, X_test, y_train, y_test = train_test_split(X_counts, y, test_size=0.3, random_state=42)

# Addestramento del modello
nb.fit(X_train, y_train)


print("\nValutazione del modello sul test set con calcolo e stampa della curva di ROC e dell'AUC")

# Predizione sui dati di test
y_pred = nb.predict(X_test)

# Calcolo dell'accuratezza
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuratezza del modello: {accuracy:.4f}")

# Predizioni probabilistiche per la curva ROC
y_prob = nb.predict_proba(X_test)[:, 1]

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
plt.title('Curva ROC per il Modello Naive Bayes\n(chiudire la finestra per continuare)')
plt.legend(loc="lower right")
plt.show()


print("\nValutazione del modello con 5-fold cross validation")

# K-Fold Cross Validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(nb, X_counts, y, cv=skf, scoring='accuracy')

# Calcolo della media e deviazione standard
accuracy_mean = scores.mean()
accuracy_std = scores.std()

# Stampa dei risultati
print(f"Accuratezza media con {5}-Fold Cross-Validation: {accuracy_mean:.4f}")
print(f"Deviazione standard dell'accuratezza: {accuracy_std:.4f}")