import subprocess
import os

# Lista dei file Python da eseguire in ordine
scripts = [
    "./python/pre_processing/last_field_cleaner.py",
    "./python/pre_processing/sd_field_cleaner.py",
    "./python/pre_processing/first_field_cleaner.py",
    "./python/pre_processing/third_field_cleaner.py", 
    "./python/pre_processing/num_words_for_texts.py",
    "./python/prolog_code/generate_kb.py",
    "./python/prolog_code/apply_rules_and_update_kb.py",
    "./python/naive_bayes/naive_bayes.py",
    "./python/random_forest/random_forest.py",
    "./python/knn/knn.py",
    "./python/k-means/k-means.py"
]


# Esegui ogni script in sequenza
for script in scripts:
    file_name = (script.split("/"))[3]
    print(f"\n Eseguendo: {file_name}")

    # Controlla se il file esiste prima di eseguirlo
    if not os.path.exists(script):
        print(f"Errore: Il file '{file_name}' non è stato trovato.")
        break  # Interrompe l'esecuzione

    # Esegui lo script
    result = subprocess.run(["python", script], text=True)
    
    # Se lo script ha dato errore, stampa lo stderr e interrompi l'esecuzione
    if result.returncode != 0:
        print(f"Errore nell'esecuzione di {script}:")
        print(result.stderr)
        break  # Interrompe l'esecuzione

else:
    # Questo blocco viene eseguito solo se tutti gli script sono stati eseguiti con successo
    print("\nTutti gli script sono stati eseguiti correttamente!")