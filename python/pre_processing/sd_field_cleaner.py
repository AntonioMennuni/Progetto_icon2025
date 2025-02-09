import pandas as pd

# Inserisci il percorso del file originale
file_path = "csv/dataset_no_last_empty_field.csv"

# Specifica il percorso per il file pulito
output_file_cleaned = "csv/dataset_no_second_empty_field.csv"

try:
    # Carica il file CSV
    data = pd.read_csv(file_path)

    # Salta la prima riga ed estrai il secondo campo
    second_field = data.iloc[1:, 1]  # Secondo campo è alla posizione indice 1
    
    # Identifica righe valide (secondo campo non nullo o vuoto)
    valid_rows = data.iloc[1:][~(second_field.isna() | second_field.str.strip().eq(""))]
    
    # Salva le righe valide in un nuovo file
    valid_rows.to_csv(output_file_cleaned, index=False)
    
    print(f"Totale righe nel file pre rimozione (esclusa la prima): {len(data) - 1}")
    print(f"Rimosse {len(data) - 1 - len(valid_rows)} righe con secondo campo nullo o vuoto.")
    print(f"File pulito salvato in: {output_file_cleaned}")
    
except Exception as e:
    print(f"Errore durante la pulizia del file: {e}")
