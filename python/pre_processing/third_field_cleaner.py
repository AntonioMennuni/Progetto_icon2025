import pandas as pd

# Inserisci il percorso del file originale
file_path = "csv/dataset_no_first_empty_field.csv"

# Specifica il percorso per il file pulito
output_file_cleaned = "csv/clean_dataset.csv"

try:
    # Carica il file CSV
    data = pd.read_csv(file_path)
    
    # Estrai il terzo campo e ignora la prima riga di intestazione
    second_field = data.iloc[:, 2]
    
    # Identifica righe valide (terzo campo non nullo o vuoto)
    valid_rows = data[~(second_field.isna() | second_field.str.strip().eq(""))]

    # Salva le righe valide in un nuovo file
    valid_rows.to_csv(output_file_cleaned, index=False)

    print(f"Rimosse {len(data) - len(valid_rows)} righe con terzo campo nullo o vuoto.")
    print(f"File pulito salvato in: {output_file_cleaned}")
    
except Exception as e:
    print(f"Errore durante la pulizia del file: {e}")



    




