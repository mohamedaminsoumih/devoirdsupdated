import re
import os
import pandas as pd
from tqdm import tqdm
from q2 import download_audio, cut_audio
from typing import List


import pandas as pd
from typing import List

import pandas as pd
from typing import List

def filter_df(csv_path: str, label: str) -> pd.DataFrame:
    """
    Écrivez une fonction qui prend le chemin vers le csv traité et renvoie un DataFrame avec seulement les rangées
    qui contiennent l'étiquette `label`.

    Arguments :
    - csv_path : Chemin vers le fichier CSV
    - label : L'étiquette à filtrer

    Retourne :
    - Un DataFrame avec les lignes qui contiennent le `label`
    """
    # Lecture du fichier CSV dans un DataFrame
    df = pd.read_csv(csv_path)
    
    # Filtrer les lignes qui contiennent le label dans la colonne "positive_labels"
    filtered_df = df[df['positive_labels'].str.contains(label)]
    
    return filtered_df




import os
import pandas as pd
from tqdm import tqdm
from typing import List

# Assurez-vous d'avoir importé vos fonctions précédentes:
# - filter_df
# - download_audio
# - cut_audio

def data_pipeline(csv_path: str, label: str) -> None:
    """
    Pipeline de traitement des vidéos avec une étiquette donnée :
    1. Télécharge la vidéo à <label>_raw/<ID>.mp3
    2. Coupe le segment audio et l'enregistre dans <label>_cut/<ID>.mp3

    Arguments:
    - csv_path : Chemin vers le fichier CSV contenant les segments à traiter
    - label : Étiquette à filtrer et traiter
    """
    # Filtrer les lignes contenant le label
    df = filter_df(csv_path, label)
    
    # Créer les dossiers si non existants
    raw_dir = f"{label}_raw"
    cut_dir = f"{label}_cut"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(cut_dir, exist_ok=True)

    # Itérer sur les lignes du DataFrame filtré avec une barre de progression
    for _, row in tqdm(df.iterrows(), total=len(df)):
        YTID = row['YTID']
        start = row['start_seconds']
        end = row['end_seconds']

        raw_audio_path = f"{raw_dir}/{YTID}.mp3"
        cut_audio_path = f"{cut_dir}/{YTID}.mp3"

        try:
            # 1. Télécharger la vidéo si elle n'existe pas déjà
            download_audio(YTID, raw_audio_path)
            
            # 2. Couper l'audio pour ne garder que le segment souhaité
            cut_audio(raw_audio_path, cut_audio_path, start, end)
        except Exception as e:
            print(f"Erreur avec la vidéo {YTID} : {e}")
            continue  # Passer à la prochaine vidéo en cas d'erreur



def rename_files(path_cut: str, start: float, end: float) -> None:
    """
    Renomme les fichiers dans le dossier spécifié pour inclure les informations de début, de fin et de durée.
    """
    # Vérifier si le chemin existe
    if not os.path.exists(path_cut):
        print(f"Erreur : Le chemin spécifié n'existe pas : {path_cut}")
        return

    for filename in os.listdir(path_cut):
        if filename.endswith(".mp3"):
            # Calculer la durée du segment
            length = end - start
            
            # Extraire l'identifiant YouTube (avant ".mp3")
            ytid = filename.split('.')[0]
            
            # Nouveau nom de fichier
            new_filename = f"{ytid}_{int(start)}_{int(end)}_{int(length)}.mp3"
            
            # Chemin complet vers les fichiers
            old_path = os.path.join(path_cut, filename)
            new_path = os.path.join(path_cut, new_filename)
            
            # Vérifier si le fichier existe avant de renommer
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(f"Renamed {filename} to {new_filename}")
            else:
                print(f"Erreur : Le fichier {old_path} n'existe pas.")

# Exemple d'utilisation avec le chemin correct
rename_files("/Users/mohamedaminsoumih/Desktop/devoirds/data", start=0, end=30)





if __name__ == "__main__":
    print(filter_df("audio_segments_clean.csv", "Laughter"))
    data_pipeline("audio_segments_clean.csv", "Laughter")
    rename_files("Laughter_cut", "audio_segments_clean.csv")
