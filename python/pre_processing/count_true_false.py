import pandas as pd

# Inserisci il percorso del file
file_path = "csv/clean_dataset.csv"

try:
    # Carica il file CSV
    data = pd.read_csv(file_path)

    # Salta la prima riga ed estrai l'ultimo campo
    last_field = data.iloc[1:, -1]
    
    # Normalizza i valori: rimuove spazi e converte in minuscolo
    normalized_last_field = last_field.str.strip().str.lower()
    
    # Conta i valori "true" e "fake"
    true_count = normalized_last_field.eq("true").sum()
    fake_count = normalized_last_field.eq("fake").sum()
    
    # Stampa i risultati
    print(f"Righe con 'true': {true_count}")
    print(f"Righe con 'fake': {fake_count}")
    print(f"Totale righe nel file (esclusa la prima): {len(data) - 1}")
    
except Exception as e:
    print(f"Errore nell'analisi del file: {e}")

