import pandas as pd
import os

def create_prolog_kb(csv_file, kb_file):
    # Leggere il dataset
    df = pd.read_csv(csv_file)

    # Creare la directory per il file di output se non esiste
    os.makedirs(os.path.dirname(kb_file), exist_ok=True)

    # Aprire il file di output per scrivere i fatti
    with open(kb_file, 'w', encoding='ISO-8859-1') as f:
        # Dichiarazione di predicati dinamici
        f.write("% Predicati dinamici\n")
        f.write(":- dynamic suspicious_political_news/2.\n")
        f.write(":- dynamic news/5.\n")
        f.write(":- dynamic suspicious_clickbait/2.\n\n")

        #scrivi i fatti nel file prolog dei fatti
        for _, row in df.iterrows():
            row_id = row['id']
            text = row['text'].replace('"', '\"').replace('\n', ' ')
            subject = row['subject'].strip()
            tof = row['tof']
            num_words = row['num_words']
            fact = f"news({row_id}, \"{text}\", \"{subject}\", \"{tof}\", {num_words}).\n"
            f.write(fact)


#crea i percorsi per il file csv e il file prolog
base_path = os.path.abspath(os.path.dirname(__file__))
csv_path = os.path.abspath(os.path.join(base_path, '..\\..', 'csv'))
prolog_path = os.path.abspath(os.path.join(base_path, '..\\..'))
dataset_path = os.path.join(csv_path, 'clean_dataset_with_num_words.csv')
kb_path = os.path.join(prolog_path, 'facts.pl')

# Creare la KB in formato Prolog
create_prolog_kb(dataset_path, kb_path)
print(f"La KB è stata creata con successo e salvata in {kb_path}.")