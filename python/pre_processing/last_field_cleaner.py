import pandas as pd

# Inserisci il percorso del file originale
file_path = "csv/Fake_Real.csv"

# Specifica il percorso per il file pulito
output_file = "csv/dataset_no_last_empty_field.csv"

try:
    # Carica il file CSV
    data = pd.read_csv(file_path)

    # Salta la prima riga ed estrai il secondo campo
    last_field = data.iloc[1:, -1]
    
    # Normalizza i valori: rimuove spazi e converte in minuscolo
    normalized_last_field = last_field.str.strip().str.lower()
    
    # Identifica le righe valide
    valid_rows = data.iloc[1:][normalized_last_field.isin(["true", "fake"])]
    
    # Salva le righe valide in un nuovo file
    valid_rows.to_csv(output_file, index=False)
    
    print(f"Rimosse {len(data) - 1 - len(valid_rows)} righe non valide.")
    print(f"File pulito salvato in: {output_file}")
    
except Exception as e:
    print(f"Errore durante la pulizia del file: {e}")
