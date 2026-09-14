import numpy as np
import pandas as pd

np.random.seed(42)

n_records = 150
prenoms = [
    "Lucas",
    "Emma",
    "Hugo",
    "Chloé",
    "Enzo",
    "Léa",
    "Nathan",
    "Manon",
    "Théo",
    "Camille",
]
noms = [
    "Martin",
    "Bernard",
    "Thomas",
    "Petit",
    "Robert",
    "Richard",
    "Durand",
    "Dubois",
    "Moreau",
    "Laurent",
]

sections = ["Football", "Tennis", "Basketball", "Judo", "Danse", "Fitness"]
villes = [
    "Grabels",
    "Saint-Gély-du-Fesc",
    "Montpellier",
    "Saint-Clément-de-Rivière",
]
statuts = ["Payé", "En attente", "Incomplet"]

dates = pd.date_range(start="2026-01-01", end="2026-09-10", freq="D")

data = {
    "ID_Adherent": [f"ADH-{1000+i}" for i in range(n_records)],
    "Nom": [
        f"{np.random.choice(prenoms)} {np.random.choice(noms)}"
        for _ in range(n_records)
    ],
    "Ville": np.random.choice(villes, n_records, p=[0.3, 0.3, 0.3, 0.1]),
    "Section": np.random.choice(sections, n_records),
    "Tarif (€)": np.random.choice([150, 180, 220, 250], n_records),
    "Statut": np.random.choice(statuts, n_records, p=[0.7, 0.2, 0.1]),
    "Date_Inscription": np.random.choice(dates, n_records),
}

df = pd.DataFrame(data)
df.to_csv("adhesions_club.csv", index=False)
print("Données de test 'adhesions_club.csv' générées avec succès !")