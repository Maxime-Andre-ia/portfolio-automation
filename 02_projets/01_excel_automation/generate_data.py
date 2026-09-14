import os
import random
import pandas as pd
from faker import Faker

fake = Faker('fr_FR')
os.makedirs("fichiers_entree", exist_ok=True)

services = ["Conseil", "Formation", "Audit", "Développement"]
statuts = ["Payé", "En attente", "PAYE", " En attente ", "Payé "]

for i in range(1, 6):
    data = []
    for _ in range(25):
        data.append({
            "Date": fake.date_between(start_date='-30d', end_date='today').strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y"])),
            "Client": fake.company(),
            "Service": random.choice(services),
            "Montant HT": random.choice([150, 300, 450, 600, None]),
            "Statut": random.choice(statuts)
        })
    df = pd.DataFrame(data)
    # Ajout de doublons volontaires pour la démonstration
    df = pd.concat([df, df.head(2)], ignore_index=True)
    df.to_excel(f"fichiers_entree/rapport_semaine_{i}.xlsx", index=False)

print("5 fichiers Excel de test générés dans 'fichiers_entree/' !")