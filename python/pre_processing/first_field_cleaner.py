import pandas as pd

# Percorsi file
file_path = "csv/dataset_no_second_empty_field.csv"
output_file = "csv/dataset_no_first_empty_field.csv"

try:
    # Caricare il CSV
    data = pd.read_csv(file_path)

    # Filtrare le righe con 'id' numerico intero (escludendo NaN)
    valid_rows = data[data["id"].notna() & (data["id"] % 1 == 0)].copy()

    # Convertire 'id' in int per rimuovere il .0
    valid_rows["id"] = valid_rows["id"].astype(int)

    # Salvare il CSV specificando il tipo di dati
    valid_rows.to_csv(output_file, index=False, float_format="%.0f")

    print(f"File pulito salvato in: {output_file}")
    print(f"Rimosse {len(data) - len(valid_rows)} righe non valide.")

except Exception as e:
    print(f"Errore: {e}")
