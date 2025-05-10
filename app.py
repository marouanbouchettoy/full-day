import os
import subprocess
from random import randint, choice, random
from datetime import datetime, timedelta

# Définir les dates de début et de fin
start_date = datetime(2025, 5, 9)
end_date = datetime(2025, 6, 28)

# Liste de messages de commit aléatoires
commit_messages = [
    "Improved performance.",
    "Fixed a bug in the system.",
    "Added a new feature.",
    "Refactored some code.",
    "Updated documentation.",
    "Optimized database queries.",
    "Removed deprecated functions.",
    "Enhanced UI components.",
    "Corrected typos in code.",
    "Improved logging mechanism."
]

# Vérifier si le répertoire est un dépôt Git
if not os.path.isdir(".git"):
    print("Erreur : Ce script doit être exécuté dans un dépôt Git valide.")
    exit(1)

# Boucle pour chaque jour dans la plage de dates spécifiée
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')

    # Définir la probabilité d'avoir des commits un jour donné
    if random() < 0.8:  # 80 % de probabilité d'avoir des commits ce jour-là
        # Générer un nombre aléatoire de commits pour la journée
        num_commits = randint(1, 10)  # Nombre de commits plus variable
        for _ in range(num_commits):
            # Générer une heure, minute et seconde aléatoires
            random_hour = randint(0, 23)
            random_minute = randint(0, 59)
            random_second = randint(0, 59)
            commit_datetime = datetime(
                current_date.year,
                current_date.month,
                current_date.day,
                random_hour,
                random_minute,
                random_second
            )
            commit_date_str = commit_datetime.strftime('%Y-%m-%dT%H:%M:%S')

            # Écrire dans le fichier
            with open('file.txt', 'a') as file:
                file.write(f'Commit on {commit_date_str}\n')

            # Ajouter les changements
            subprocess.run(['git', 'add', '.'], check=True)

            # Faire le commit avec une date spécifique
            commit_message = choice(commit_messages)
            subprocess.run(
                ['git', 'commit', '--date', commit_date_str, '-m', commit_message],
                check=True
            )

    # Passer au jour suivant
    current_date += timedelta(days=1)

# Pousser tous les commits vers la branche principale
try:
    subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Erreur lors du push : {e}")
