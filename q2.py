import youtube_dl
import ffmpeg
import pandas as pd
import numpy as np
import csv
import threading
from tqdm import tqdm
from os.path import exists


import os
import youtube_dl

def download_audio(YTID: str, path: str) -> None:
    """
    Télécharge l'audio de la vidéo YouTube avec un identifiant donné et l'enregistre dans le dossier donné par `path`.
    Télécharge l'audio en mp3. Si le fichier existe déjà, la fonction retourne sans télécharger à nouveau.
    
    Arguments :
    - YTID : Identifiant YouTube de la vidéo à télécharger.
    - path : Le chemin d'accès où l'audio sera enregistré.
    """
    # Vérifie si le fichier existe déjà
    if os.path.exists(path):
        print(f"Le fichier {path} existe déjà.")
        return
    
    # URL de la vidéo YouTube
    url = f'https://www.youtube.com/watch?v={YTID}'
    
    # Options de téléchargement pour youtube_dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,  # Garde la sortie silencieuse
        'noplaylist': True  # Ne télécharge pas les playlists
    }
    
    # Téléchargement de l'audio
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"L'audio a été téléchargé avec succès et enregistré à {path}.")
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'audio : {e}")



import ffmpeg

def cut_audio(in_path: str, out_path: str, start: float, end: float) -> None:
    """
    Coupe l'audio de in_path pour n'inclure que le segment de start à end et l'enregistre dans out_path.

    Arguments :
    - in_path : Chemin du fichier audio à couper.
    - out_path : Chemin du fichier pour enregistrer l'audio coupé.
    - start : Indique le début de la séquence (en secondes).
    - end : Indique la fin de la séquence (en secondes).
    """
    try:
        # Utilisation de ffmpeg pour couper l'audio
        (
            ffmpeg
            .input(in_path, ss=start, to=end)  # ss = start, to = end
            .output(out_path)
            .run(overwrite_output=True, quiet=True)
        )
        print(f"L'audio a été coupé et enregistré à {out_path}.")
    except Exception as e:
        print(f"Erreur lors de la coupe de l'audio : {e}")
