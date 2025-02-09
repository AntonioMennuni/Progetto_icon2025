import pandas as pd

# Caricamento del dataset
dataset_path = "csv/clean_dataset.csv"
data = pd.read_csv(dataset_path, encoding='ISO-8859-1')

output_dataset_path = "csv/clean_dataset_with_num_words.csv"

# Verifica che il dataset abbia la colonna 'text'
if 'text' not in data.columns:
    raise ValueError("Il dataset non contiene la colonna 'text'.")

# Aggiungi la colonna 'num_words' che conta il numero di parole per ogni riga
data['num_words'] = data['text'].apply(lambda x: len(str(x).split()))

# Riordina le colonne per posizionare 'num_words' dopo 'tof'
columns_order = ['id', 'text', 'subject', 'tof', 'num_words']
data = data[columns_order]

# Salva il dataset aggiornato in un nuovo file CSV
data.to_csv(output_dataset_path, index=False)
