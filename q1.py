import json
import pandas as pd


import json
import pandas as pd


def count_labels(labels: str) -> int:
    """
    Étant donné une chaine de charactères d'étiquettes non traitées, retourne le nombre d'étiquettes distinctes.

    Par exemple:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> 3
    """
    return len(set(labels.split(',')))



import json

def convert_id(ID: str) -> str:
    """
    Créez une fonction qui prend un ID d'étiquette (par exemple "/m/09x0r") et renvoie le nom d'étiquette correspondant (par exemple "Speech").
    """
    with open('/Users/mohamedaminsoumih/Desktop/devoirds/data/audio_segments.csv', 'r') as f:
        ontology = json.load(f)
    
    # Parcourt l'ontologie pour trouver l'ID correspondant
    for item in ontology:
        if item['id'] == ID:
            return item['name']
    
    # Retourne une chaîne vide si l'ID n'est pas trouvé
    return ""


def convert_ids(labels: str) -> str:
    """
    À l'aide de convert_id(), créez une fonction qui prend les colonnes d'étiquettes (c'est-à-dire une chaîne de charactères d'ID d'étiquettes séparées par des virgules)
    et renvoie une chaîne de noms d'étiquettes, séparés par des tubes "|".
    """
    # Sépare les ID d'étiquettes
    ids = labels.split(',')
    
    # Applique convert_id() à chaque ID et les joint par des tubes "|"
    return '|'.join([convert_id(label) for label in ids])



import pandas as pd

def contains_label(labels: pd.Series, label: str) -> pd.Series:
    """
    Créez une fonction qui prend une pandas Series de chaînes de charactères où chaque chaîne de charactères est formatée comme ci-dessus
    (c'est-à-dire "|" sépare les noms d'étiquettes comme "Music|Skateboard|Speech") et renvoie une pandas Series avec juste
    les valeurs qui incluent `label`.
    """
    # Utiliser str.contains pour filtrer les valeurs qui contiennent le label
    return labels[labels.str.contains(label)]



import pandas as pd

def get_correlation(labels: pd.Series, label_1: str, label_2: str) -> float:
    # Vérifier que labels n'est pas None et qu'il est de type pd.Series
    if labels is None or not isinstance(labels, pd.Series):
        raise ValueError("L'argument 'labels' doit être une pandas Series valide.")

    # Vérifie si les labels existent dans la série
    if label_1 not in labels.values or label_2 not in labels.values:
        raise ValueError(f"Erreur : Les étiquettes '{label_1}' ou '{label_2}' ne sont pas présentes dans la série.")

    total_label_1 = (labels == label_1).sum()

    # Si le total est zéro, renvoie 0 pour éviter la division par zéro
    if total_label_1 == 0:
        return 0.0

    # Compter les occurrences où les deux labels coexistent
    co_occurrence = ((labels == label_1) & (labels == label_2)).sum()

    return co_occurrence / total_label_1




if __name__ == "__main__":
    print(count_labels("/m/04rlf,/m/06_fw,/m/09x0r"))
    print(convert_id("/m/04rlf"))
    print(convert_ids("/m/04rlf,/m/06_fw,/m/09x0r"))

    series = pd.Series([
        "Music|Skateboard|Speech",
        "Voice|Speech",
        "Music|Piano"
    ])
    print(contains_label(series, "Music"))
    print(get_correlation(series, "Music", "Piano"))


def contains_label(labels: pd.Series, label: str) -> pd.Series:
    """
    Créez une fonction qui prend une pandas Series de chaînes de charactères où chaque chaîne de charactères est formatée comme ci-dessus
    (c'est-à-dire "|" sépare les noms d'étiquettes comme "Music|Skateboard|Speech") et renvoie une pandas Series avec juste
    les valeurs qui incluent `label`.

    Par exemple, étant donné le label "Music" et la série suivante :
    "Music|Skateboard|Speech"
    "Voice|Speech"
    "Music|Piano"

    la fonction devrait retourner
    "Music|Skateboard|Speech"
    "Music|Piano"
    """
    # TODO
    pass


def get_correlation(labels: pd.Series, label_1: str, label_2: str) -> float:
    """
    Créez une fonction qui, avec une pandas Series comme décrit ci-dessus, renvoie la proportion de rangées
    avec label_1 qui ont également label_2. Utilisez la fonction que vous avez créée ci-dessus.

    Par exemple, supposons que la pandas Series comporte 1 000 valeurs, dont 120 ont label_1. Si 30 des 120
    ont label_2, votre fonction doit renvoyer 0,25.
    """
    # TODO
    pass


if __name__ == "__main__":
    print(count_labels("/m/04rlf,/m/06_fw,/m/09x0r"))
    print(convert_id("/m/04rlf"))
    print(convert_ids("/m/04rlf,/m/06_fw,/m/09x0r"))

    series = pd.Series([
        "Music|Skateboard|Speech",
        "Voice|Speech",
        "Music|Piano"
    ])
    print(contains_label(series, "Music"))
    print(get_correlation(series, "Music", "Piano"))
