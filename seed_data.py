# =========================================================
# seed_data.py — Données par défaut pour EduStat
# Exécuter une seule fois : python seed_data.py
# =========================================================

import sqlite3
from datetime import datetime
import random

NOM_BDD = "edustat.db"

# ----------------------------------------------------------
# 50 étudiants fictifs (inspirés de noms camerounais)
# Tu peux modifier, ajouter ou supprimer des lignes
# ----------------------------------------------------------
ETUDIANTS = [
    # (nom, sexe, filiere, niveau, matiere, note, heures_etude, presence)
    ("Mbarga Jean-Pierre",    "Masculin", "Informatique",           "L2", "Analyse de données",      14.5, 15, 85),
    ("Nguema Astrid",         "Féminin",  "Informatique",           "L2", "Analyse de données",      17.0, 22, 95),
    ("Tchamda Boris",         "Masculin", "Informatique",           "L2", "Analyse de données",       9.5, 8,  60),
    ("Kamga Laure",           "Féminin",  "Informatique",           "L2", "Analyse de données",      13.0, 12, 78),
    ("Essono Paul",           "Masculin", "Informatique",           "L2", "Analyse de données",      11.5, 10, 70),
    ("Bikié Carine",          "Féminin",  "Informatique",           "L2", "Analyse de données",      16.5, 20, 92),
    ("Nkoulou Rodrigue",      "Masculin", "Informatique",           "L2", "Analyse de données",       7.0, 5,  45),
    ("Ondoa Mireille",        "Féminin",  "Informatique",           "L2", "Analyse de données",      15.5, 18, 88),
    ("Abanda Christian",      "Masculin", "Informatique",           "L2", "Analyse de données",      12.0, 11, 75),
    ("Fouda Stéphanie",       "Féminin",  "Informatique",           "L2", "Analyse de données",      18.5, 25, 98),

    ("Djoumessi Armel",       "Masculin", "Mathématiques",          "L3", "Algèbre linéaire",        16.0, 20, 90),
    ("Tsanga Inès",           "Féminin",  "Mathématiques",          "L3", "Algèbre linéaire",        19.0, 28, 100),
    ("Owona Serge",           "Masculin", "Mathématiques",          "L3", "Algèbre linéaire",        10.0, 9,  65),
    ("Mbassi Flore",          "Féminin",  "Mathématiques",          "L3", "Algèbre linéaire",        14.0, 16, 82),
    ("Bekolo Didier",         "Masculin", "Mathématiques",          "L3", "Algèbre linéaire",         8.5, 7,  55),
    ("Ngo Biyong Sylvie",     "Féminin",  "Mathématiques",          "L3", "Algèbre linéaire",        17.5, 23, 95),

    ("Feudjio Gaëtan",        "Masculin", "Économie-Gestion",       "L1", "Microéconomie",           11.0, 10, 72),
    ("Ateba Sandrine",        "Féminin",  "Économie-Gestion",       "L1", "Microéconomie",           13.5, 14, 80),
    ("Nkoa Joël",             "Masculin", "Économie-Gestion",       "L1", "Microéconomie",            6.5, 4,  40),
    ("Mvondo Pauline",        "Féminin",  "Économie-Gestion",       "L1", "Microéconomie",           15.0, 17, 87),
    ("Biyong Thierry",        "Masculin", "Économie-Gestion",       "L1", "Microéconomie",           10.5, 9,  68),
    ("Essama Rachel",         "Féminin",  "Économie-Gestion",       "L1", "Microéconomie",           12.5, 13, 78),

    ("Nanga Wilfried",        "Masculin", "Physique-Chimie",        "L2", "Mécanique quantique",      9.0, 8,  58),
    ("Mbam Aurelie",          "Féminin",  "Physique-Chimie",        "L2", "Mécanique quantique",     14.0, 15, 83),
    ("Zambo Franck",          "Masculin", "Physique-Chimie",        "L2", "Mécanique quantique",     12.0, 12, 74),
    ("Edo'o Patricia",        "Féminin",  "Physique-Chimie",        "L2", "Mécanique quantique",     16.5, 21, 91),

    ("Ndoumou Kevin",         "Masculin", "Sciences de la Vie",     "L1", "Biologie cellulaire",     13.0, 13, 79),
    ("Olinga Berthe",         "Féminin",  "Sciences de la Vie",     "L1", "Biologie cellulaire",     17.0, 22, 94),
    ("Mekongo Jules",         "Masculin", "Sciences de la Vie",     "L1", "Biologie cellulaire",      8.0, 6,  50),
    ("Ayissi Diane",          "Féminin",  "Sciences de la Vie",     "L1", "Biologie cellulaire",     15.5, 19, 89),

    ("Ndjock Alexis",         "Masculin", "Informatique",           "M1", "Machine Learning",        18.0, 30, 97),
    ("Bebey Christelle",      "Féminin",  "Informatique",           "M1", "Machine Learning",        15.0, 18, 85),
    ("Tchamba Rostand",       "Masculin", "Informatique",           "M1", "Machine Learning",        11.5, 10, 70),
    ("Menguele Ornella",      "Féminin",  "Informatique",           "M1", "Machine Learning",        14.0, 16, 82),
    ("Ekambi Thierry",        "Masculin", "Informatique",           "M1", "Machine Learning",        16.5, 24, 93),

    ("Zanga Alice",           "Féminin",  "Lettres & Sciences Humaines", "L2", "Linguistique",       14.5, 15, 84),
    ("Manga Edouard",         "Masculin", "Lettres & Sciences Humaines", "L2", "Linguistique",       10.0, 9,  66),
    ("Ngo Mboula Cécile",     "Féminin",  "Lettres & Sciences Humaines", "L2", "Linguistique",       16.0, 20, 90),
    ("Bello Simon",           "Masculin", "Lettres & Sciences Humaines", "L2", "Linguistique",        7.5, 5,  48),

    ("Tatchou Vanessa",       "Féminin",  "Économie-Gestion",       "M1", "Économétrie",             17.5, 26, 96),
    ("Eto'o Junior",          "Masculin", "Économie-Gestion",       "M1", "Économétrie",             13.5, 14, 80),
    ("Nkoa Madeleine",        "Féminin",  "Économie-Gestion",       "M1", "Économétrie",             12.0, 11, 73),
    ("Mvele Patrick",         "Masculin", "Économie-Gestion",       "M1", "Économétrie",              9.5, 8,  60),

    ("Ayolo Nadia",           "Féminin",  "Mathématiques",          "M2", "Probabilités avancées",   18.5, 30, 98),
    ("Biwole Ernest",         "Masculin", "Mathématiques",          "M2", "Probabilités avancées",   15.5, 20, 87),
    ("Nkouaga Jeanne",        "Féminin",  "Mathématiques",          "M2", "Probabilités avancées",   14.0, 17, 83),

    ("Essama Rodrigue",       "Masculin", "Informatique",           "L3", "Bases de données",        13.5, 14, 80),
    ("Moukam Ghislaine",      "Féminin",  "Informatique",           "L3", "Bases de données",        16.0, 21, 91),
    ("Onana Christian",       "Masculin", "Informatique",           "L3", "Bases de données",        10.5, 9,  67),
    ("Beng Martine",          "Féminin",  "Informatique",           "L3", "Bases de données",        15.0, 18, 85),
]

# ----------------------------------------------------------
# INSERTION DANS LA BASE DE DONNÉES
# ----------------------------------------------------------
def seeder():
    connexion = sqlite3.connect(NOM_BDD)
    curseur = connexion.cursor()

    # Vérifie si la table existe déjà
    curseur.execute("SELECT COUNT(*) FROM performances")
    nb_existant = curseur.fetchone()[0]

    if nb_existant > 0:
        print(f"⚠️  La base contient déjà {nb_existant} entrée(s).")
        choix = input("Voulez-vous QUAND MÊME ajouter les données par défaut ? (o/n) : ")
        if choix.lower() != "o":
            print("❌ Opération annulée.")
            connexion.close()
            return

    # Insertion de chaque étudiant
    for i, (nom, sexe, filiere, niveau, matiere, note, heures, presence) in enumerate(ETUDIANTS):
        # Date fictive échelonnée sur les dernières semaines
        date = f"{random.randint(1,28):02d}/{random.randint(1,4):02d}/2025 {random.randint(8,17):02d}:00"
        curseur.execute("""
            INSERT INTO performances
                (nom, filiere, niveau, matiere, note, heures_etude, taux_presence, sexe, date_saisie)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, filiere, niveau, matiere, note, heures, presence, sexe, date))
        print(f"  ✅ [{i+1:02d}] {nom} — {note}/20")

    connexion.commit()
    connexion.close()
    print(f"\n🎉 {len(ETUDIANTS)} étudiants insérés avec succès dans '{NOM_BDD}' !")
    print("▶️  Lance maintenant : streamlit run app.py")


if __name__ == "__main__":
    print("=" * 55)
    print("  EduStat — Insertion des données par défaut")
    print("=" * 55)
    seeder()
