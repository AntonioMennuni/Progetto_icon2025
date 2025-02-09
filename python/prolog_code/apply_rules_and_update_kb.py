#import csv
from pyswip import Prolog
import os
import pandas as pd


# Funzione per eseguire la regola Prolog e ottenere i risultati
def execute_rule(prolog,query):
    print("Esecuzione della regola...")    
    # Recupera tutte le notizie sospette (Id)
    news = list(prolog.query(f"{query}"))
    print("regola eseguita")
    # Estrai gli Id delle notizie sospette
    detected_news_id = [r['Id'] for r in news]

    return detected_news_id



# Funzione per aggiungere il predicato 'predicate' nel file Prolog
def update_prolog_facts(facts_file, detected_news_id,predicate):
    with open(facts_file, "a", encoding="ISO-8859-1") as f:
        with open(facts_file, "r", encoding="ISO-8859-1") as f_read:
            existing_facts = f_read.readlines()
        
        for line in existing_facts:
            if line.startswith("news"):
                # Estrai l'ID dalla riga del fatto
                parts = line.split(",")
                news_id = int(parts[0].split("(")[1])
                
                # Aggiungi il predicato 'suspicious_political_news'
                if news_id in detected_news_id:
                    f.write(f"\n{predicate}({news_id}, 'true').")
                else:
                    f.write(f"\n{predicate}({news_id}, 'false').")



# Funzione per esportare le notizie in un file CSV, includendo il campo 'suspicious_political_news'
def export_as_csv_political_rule(facts_file, output_csv_file, prolog):
    print("Esportazione in CSV con Pandas...")

    # Lista per memorizzare i dati
    data = []

    # Legge i fatti dal file Prolog
    with open(facts_file, "r", encoding="ISO-8859-1") as f_read:
        existing_facts = f_read.readlines()

    for line in existing_facts:
        if line.startswith("news"):
            # Estrai i campi dal fatto 
            parts = line.split(",")
            news_id = int(parts[0].split("(")[1])
            text = parts[1].strip()
            subject = parts[2].strip()
            tof = parts[3].strip()
            num_words = int(parts[4].split(")")[0].strip())

            # Esegui la query per ottenere il valore di 'suspicious_political_news'
            query_result = list(prolog.query(f"suspicious_political_news({news_id}, S)"))
            suspicious_status = query_result[0]['S'] if query_result else 'false'

            # Aggiungi i dati alla lista
            data.append([news_id, text.replace('"',""), subject.replace('"',""), tof.replace('"',""), num_words, suspicious_status])

    # Creiamo un DataFrame con i dati raccolti
    df = pd.DataFrame(data, columns=["id", "text", "subject", "tof", "num_words", "suspicious_political_news"])

    # Esportiamo in CSV con intestazione, senza virgolette indesiderate
    df.to_csv(output_csv_file, index=False, quoting=3, encoding="ISO-8859-1")

    print(f"File CSV esportato correttamente in {output_csv_file}.")



# Funzione per esportare le notizie in un file CSV, includendo il campo 'suspicious_clickbait_news'
def export_as_csv_clickbait_rule(facts_file, output_csv_file, prolog):
    print("Esportazione in CSV con Pandas...")

    # Lista per memorizzare i dati
    data = []

    # Legge i fatti dal file Prolog
    with open(facts_file, "r", encoding="ISO-8859-1") as f_read:
        existing_facts = f_read.readlines()

    for line in existing_facts:
        if line.startswith("news"):
            # Estrai i campi dal fatto 
            parts = line.split(",")
            news_id = int(parts[0].split("(")[1])
            text = parts[1].strip()
            subject = parts[2].strip()
            tof = parts[3].strip()
            num_words = int(parts[4].split(")")[0].strip())
            #suspicious_political_news = parts[4].split(")")[0].strip()

            # Esegui la query per ottenere il valore di 'suspicious_clickbait_news'
            query_result = list(prolog.query(f"suspicious_clickbait_news({news_id}, S)"))
            suspicious_status = query_result[0]['S'] if query_result else 'false'

            # Aggiungi i dati alla lista
            data.append([news_id, suspicious_status])

    # Creiamo un DataFrame con i dati raccolti
    df = pd.DataFrame(data, columns=["id", "suspicious_clickbait_news"])

    # Esportiamo in CSV con intestazione, senza virgolette indesiderate
    df.to_csv(output_csv_file, index=False, quoting=3, encoding="ISO-8859-1")

    print(f"File CSV esportato correttamente in {output_csv_file}.")



# Unisce il contenuto di due file csv in uno solo preservando tutte le colonne
def mergeNews(file1, file2, output_file):
    # Leggiamo i due CSV in DataFrame
    df1 = pd.read_csv(file1, encoding="ISO-8859-1")
    df2 = pd.read_csv(file2, encoding="ISO-8859-1")

    # Uniamo i DataFrame sulla colonna "id" con una join esterna
    df_merged = pd.merge(df1, df2, on="id", how="left")

    # Esporta il nuovo file CSV
    df_merged.to_csv(output_file, index=False, encoding="ISO-8859-1")

    print(f"File uniti correttamente: {output_file}")



# # Inizializza e carica i fatti e le regole in Prolog
prolog = Prolog()

# Carica i file in Prolog
prolog.consult("facts.pl")
prolog.consult("rules.pl")

facts_path="facts.pl"
base_path = os.path.abspath(os.path.dirname(__file__))
csv_path = os.path.abspath(os.path.join(base_path, '..\\..', 'csv'))
output_csv_file_1 = os.path.join(csv_path, 'dataset_with_political_suspicious.csv')
output_csv_file_2 = os.path.join(csv_path, 'dataset_with_clickbait_suspicious.csv')

print("L'ESECUZIONE POTREBBE RICHIEDERE ALCUNI MINUTI.. \n ATTENDERO PREGO!")


# REGOLA 1 (NOTIZIE POLITICHE SOSPETTE)

# Esegui la regola su Prolog per ottenere gli Id delle notizie sospette
suspicious_news_id = execute_rule(prolog,"detect_suspicious_political_news(Id)")

# Aggiungi il predicato 'suspicious_political_news' nel file di fatti
update_prolog_facts(facts_path, suspicious_news_id,"suspicious_political_news") 
prolog.consult("facts.pl")

# Esporta i dati in un file CSV
export_as_csv_political_rule(facts_path, output_csv_file_1, prolog)

print("fine prima regola")


# REGOLA 2 (NOTIZIE CLICKBAIT SOSPETTE)

# Esegui la regola su Prolog per ottenere gli Id delle notizie sospette
suspicious_news_id = execute_rule(prolog,"detect_suspicious_clickbait(Id)")

# Aggiungi il predicato 'suspicious_clickbait_news' nel file dei fatti
update_prolog_facts(facts_path, suspicious_news_id,"suspicious_clickbait_news") 
prolog.consult("facts.pl")

print("fine seconda regola")
print("fine update kb")

# # Esporta i dati in un file CSV
export_as_csv_clickbait_rule(facts_path, output_csv_file_2, prolog)

# Unione dei due file CSV
mergeNews(output_csv_file_1, output_csv_file_2, os.path.join(csv_path, 'final_dataset.csv'))