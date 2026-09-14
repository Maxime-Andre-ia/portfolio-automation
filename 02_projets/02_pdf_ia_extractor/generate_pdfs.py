import os
from fpdf import FPDF

os.makedirs("factures_entree", exist_ok=True)

factures = [
    {
        "num": "FAC-2026-001",
        "date": "02/09/2026",
        "echeance": "02/10/2026",
        "fournisseur": "Fournitures Occitanie SARL",
        "siret": "801 452 987 00012",
        "ville": "Montpellier",
        "client": "AS Grabels Football",
        "categorie": "Matériel & Équipement",
        "articles": [
            ("Lot de 10 ballons T5", 2, 120.00),
            ("Lot 20 chasubles fluo", 1, 65.00),
            ("Sifflets arbitre & plots", 1, 35.50),
        ],
        "statut": "Payé",
        "reglement": "Carte Bancaire",
    },
    {
        "num": "FAC-2026-002",
        "date": "05/09/2026",
        "echeance": "20/09/2026",
        "fournisseur": "Imprimerie du Lez",
        "siret": "412 789 654 00034",
        "ville": "Saint-Gély-du-Fesc",
        "client": "Foyer Rural Saint-Clément",
        "categorie": "Communication & Print",
        "articles": [
            ("Affiches A3 Rentrée (x500)", 1, 180.00),
            ("Flyers programme annuel (x2000)", 1, 240.00),
        ],
        "statut": "En attente",
        "reglement": "Virement bancaire",
    },
    {
        "num": "FAC-2026-003",
        "date": "08/09/2026",
        "echeance": "08/10/2026",
        "fournisseur": "Services Web Hérault",
        "siret": "523 112 445 00019",
        "ville": "Montpellier",
        "client": "TC Pic Saint-Loup",
        "categorie": "Informatique & Logiciel",
        "articles": [
            ("Hébergement web annuel", 1, 120.00),
            ("Maintenance serveur & nom de domaine", 1, 150.00),
        ],
        "statut": "Payé",
        "reglement": "Prélèvement automatique",
    },
    {
        "num": "FAC-2026-004",
        "date": "10/09/2026",
        "echeance": "25/09/2026",
        "fournisseur": "Espaces Verts Héraultais",
        "siret": "309 887 123 00055",
        "ville": "Grabels",
        "client": "AS Grabels Football",
        "categorie": "Entretien & Prestations",
        "articles": [
            ("Tonte et traçage terrain principal", 2, 250.00),
            ("Entretien bordures & vestiaires", 1, 180.00),
        ],
        "statut": "À payer",
        "reglement": "Chèque",
    },
    {
        "num": "FAC-2026-005",
        "date": "11/09/2026",
        "echeance": "11/10/2026",
        "fournisseur": "Bureau & Copie 34",
        "siret": "789 456 123 00088",
        "ville": "Castelnau-le-Lez",
        "client": "École de Danse Clapiers",
        "categorie": "Fournitures de bureau",
        "articles": [
            ("Cartouches d'encre HP (Pack)", 2, 95.00),
            ("Rames de papier A4 (Carton x5)", 1, 45.00),
        ],
        "statut": "Payé",
        "reglement": "Carte Bancaire",
    },
    {
        "num": "FAC-2026-006",
        "date": "12/09/2026",
        "echeance": "30/09/2026",
        "fournisseur": "Transport & Logistique Méditerranée",
        "siret": "654 321 987 00021",
        "ville": "Lattes",
        "client": "Montpellier Basket Club",
        "categorie": "Transports & Déplacements",
        "articles": [
            ("Location Minibus 9 places (2 jours)", 1, 320.00),
            ("Forfait kilométrage 500 km", 1, 110.00),
        ],
        "statut": "En attente",
        "reglement": "Virement bancaire",
    },
]


def create_facture_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # En-tête / Couleurs
    pdf.set_fill_color(31, 78, 120)  # Bleu marine
    pdf.rect(0, 0, 210, 25, style="F")

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, text="FACTURE PROFORMA", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.ln(12)
    pdf.set_text_color(0, 0, 0)

    # Infos Fournisseur & Facture
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(100, 6, text=f"Fournisseur : {data['fournisseur']}")
    pdf.cell(0, 6, text=f"FACTURE N° : {data['num']}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(100, 5, text=f"SIRET : {data['siret']}")
    pdf.cell(0, 5, text=f"Date : {data['date']}", new_x="LMARGIN", new_y="NEXT")

    pdf.cell(100, 5, text=f"Ville : {data['ville']}")
    pdf.cell(0, 5, text=f"Échéance : {data['echeance']}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(100, 5, text=f"Facturé à : {data['client']}")
    pdf.cell(0, 5, text=f"Catégorie : {data['categorie']}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)

    # Tableau des articles
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(90, 7, text="Désignation", border=1, fill=True)
    pdf.cell(25, 7, text="Qté", border=1, align="C", fill=True)
    pdf.cell(35, 7, text="Prix Unitaire HT", border=1, align="R", fill=True)
    pdf.cell(40, 7, text="Total HT", border=1, align="R", fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    total_ht = 0.0
    for desc, qte, pu in data["articles"]:
        line_total = qte * pu
        total_ht += line_total
        pdf.cell(90, 6, text=desc, border=1)
        pdf.cell(25, 6, text=str(qte), border=1, align="C")
        pdf.cell(35, 6, text=f"{pu:.2f} EUR", border=1, align="R")
        pdf.cell(40, 6, text=f"{line_total:.2f} EUR", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    tva = total_ht * 0.20
    total_ttc = total_ht + tva

    pdf.ln(5)
    # Totaux
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(115, 6, text="")
    pdf.cell(35, 6, text="Total HT :", border=0)
    pdf.cell(40, 6, text=f"{total_ht:.2f} EUR", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.cell(115, 6, text="")
    pdf.cell(35, 6, text="TVA (20%) :", border=0)
    pdf.cell(40, 6, text=f"{tva:.2f} EUR", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.cell(115, 6, text="")
    pdf.cell(35, 6, text="Total TTC :", border=0)
    pdf.cell(40, 6, text=f"{total_ttc:.2f} EUR", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    # Pied de page paiement
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, text=f"Statut : {data['statut']} | Mode de Règlement : {data['reglement']}", new_x="LMARGIN", new_y="NEXT")

    pdf.output(f"factures_entree/{data['num']}.pdf")


for f in factures:
    create_facture_pdf(f)

print("6 factures PDF enrichies et générées dans 'factures_entree/' !")