import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_curve, auc
import matplotlib.pyplot as plt

# Caricamento del dataset
df = pd.read_csv('csv/final_dataset.csv', encoding='ISO-8859-1', header=0)

# Trasformazione del testo in TF-IDF (escludendo le stopwords)
tf_idf = TfidfVectorizer(max_features=400, stop_words='english')
X_text_tf_idf = tf_idf.fit_transform(df["text"]).toarray()

# Codifica della feature categorica "subject" con one-hot encoding
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_subject = encoder.fit_transform(df[["subject"]])

# Concatenazione delle feature numeriche e trasformate
X = np.hstack((X_text_tf_idf, X_subject, df[["num_words", "suspicious_political_news", "suspicious_clickbait_news"]].values))

# Conversione 'tof' in numerico (Fake=0, True=1)
df['tof_numeric'] = df['tof'].map({'Fake': 0, 'True': 1})

# Preparazione della variabile target "tof"
y = df["tof_numeric"]

# Divisione in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Addestramento del modello Random Forest
rf = RandomForestClassifier(n_estimators=5, random_state=42, max_features="log2")
rf.fit(X_train, y_train)


print("\nValutazione del modello sul test set con calcolo e stampa della curva di ROC e dell'AUC")

# Predizione sui dati di test
y_pred = rf.predict(X_test)

# Calcolo dell'accuratezza
accuracy = accuracy_score(y_test, y_pred)

# Stampa dell'accuratezza
print(f"Accuratezza del modello: {accuracy:.4f}")

# Predizioni probabilistiche (per ottenere la probabilità per la classe positiva "True")
y_prob = rf.predict_proba(X_test)[:,1]

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
plt.title('Curva ROC per il Modello Random forest\n(chiudire la finestra per continuare)')
plt.legend(loc="lower right")
plt.show()


print("\nValutazione del modello con 5-fold cross validation")

# Impostazione della K-Fold Cross Validation
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Valutazione del modello con Cross Validation
scores = cross_val_score(rf, X, y, cv=kf, scoring='accuracy')

# Stampa dell'accuratezza media e della deviazione standard
print(f"Accuratezza media con {5}-Fold Cross-Validation: {scores.mean():.4f}")
print(f"Deviazione standard dell'accuratezza: {scores.std():.4f}")