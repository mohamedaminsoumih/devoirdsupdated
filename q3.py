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


import os
import re
import pandas as pd

def rename_files(path_cut: str, csv_path: str) -> None:
    """
    Renomme les fichiers dans path_cut pour inclure les heures de début, de fin et la longueur du segment.
    
    Arguments:
    - path_cut: Chemin vers le dossier contenant les fichiers audio coupés.
    - csv_path: Chemin vers le fichier CSV contenant les informations sur les segments audio.
    """
    # Lire le CSV
    df = pd.read_csv(csv_path)
    
    # Parcourir chaque ligne du DataFrame
    for _, row in df.iterrows():
        YTID = row['YTID']
        start_seconds = int(row['start_seconds'])
        end_seconds = int(row['end_seconds'])
        length = end_seconds - start_seconds
        
        # Construire le nom du fichier d'origine et le nom du fichier à renommer
        original_file_pattern = re.escape(YTID) + r'.*\.mp3$'
        new_filename = f"{YTID}_{start_seconds}_{end_seconds}_{length}.mp3"
        
        # Parcourir les fichiers dans le répertoire
        for filename in os.listdir(path_cut):
            # Si le fichier correspond à l'ID de la vidéo
            if re.match(original_file_pattern, filename):
                old_filepath = os.path.join(path_cut, filename)
                new_filepath = os.path.join(path_cut, new_filename)
                
                # Renommer le fichier
                os.rename(old_filepath, new_filepath)
                print(f"Renommé : {filename} -> {new_filename}")
                break



if __name__ == "__main__":
    print(filter_df("audio_segments_clean.csv", "Laughter"))
    data_pipeline("audio_segments_clean.csv", "Laughter")
    rename_files("Laughter_cut", "audio_segments_clean.csv")
