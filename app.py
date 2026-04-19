# =========================================================
# EduStat - Application de Collecte & Analyse Scolaire
# Cours   : INF 232 EC2 - Analyse de données
# Thème   : Éducation / Performances académiques
# Backend : Python + Streamlit + SQLite + Plotly
# =========================================================

import streamlit as st          # Pour créer l'interface web
import pandas as pd             # Pour manipuler les données
import sqlite3                  # Pour la base de données locale
import plotly.express as px     # Pour les graphiques interactifs
from datetime import datetime   # Pour horodater les saisies

# ----------------------------------------------------------
# CONFIGURATION DE LA PAGE (doit être en premier)
# ----------------------------------------------------------
st.set_page_config(
    page_title="EduStat 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------
# STYLE CSS PERSONNALISÉ (apparence de l'app)
# ----------------------------------------------------------
st.markdown("""
<style>
    /* En-tête principal */
    .main-header {
        background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(26,115,232,0.3);
    }
    .main-header h1 { font-size: 2.5rem; margin-bottom: 0.3rem; }
    .main-header p  { font-size: 1.1rem; opacity: 0.9; }

    /* Bandeau de mention */
    .mention-box {
        background: #e8f5e9;
        border-left: 5px solid #43a047;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .mention-fail {
        background: #ffebee;
        border-left: 5px solid #e53935;
    }
    .mention-pass {
        background: #e3f2fd;
        border-left: 5px solid #1e88e5;
    }

    /* Pied de page */
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    div[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
</style>
""", unsafe_allow_html=True)


# ===========================================================
# SECTION BASE DE DONNÉES  (toutes les fonctions SQLite)
# ===========================================================

NOM_BDD = "edustat.db"  # Fichier de base de données local

def initialiser_bdd():
    """
    Crée la base de données et la table si elles n'existent pas encore.
    Cette fonction est appelée une seule fois au démarrage.
    """
    connexion = sqlite3.connect(NOM_BDD)
    curseur = connexion.cursor()
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS performances (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            nom            TEXT    NOT NULL,
            filiere        TEXT    NOT NULL,
            niveau         TEXT    NOT NULL,
            matiere        TEXT    NOT NULL,
            note           REAL    NOT NULL,
            heures_etude   REAL    NOT NULL,
            taux_presence  REAL    NOT NULL,
            sexe           TEXT    NOT NULL,
            date_saisie    TEXT    NOT NULL
        )
    """)
    connexion.commit()
    connexion.close()


def inserer_etudiant(nom, filiere, niveau, matiere, note, heures, presence, sexe):
    """
    Enregistre les données d'un étudiant dans la base.
    Les '?' sont des paramètres sécurisés (évite les injections SQL).
    """
    connexion = sqlite3.connect(NOM_BDD)
    curseur = connexion.cursor()
    curseur.execute("""
        INSERT INTO performances
            (nom, filiere, niveau, matiere, note, heures_etude, taux_presence, sexe, date_saisie)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nom, filiere, niveau, matiere, note, heures, presence, sexe,
          datetime.now().strftime("%d/%m/%Y %H:%M")))
    connexion.commit()
    connexion.close()


def lire_donnees():
    """
    Lit toutes les données et les retourne sous forme de DataFrame Pandas.
    Un DataFrame = tableau à lignes et colonnes, comme Excel.
    """
    connexion = sqlite3.connect(NOM_BDD)
    df = pd.read_sql("SELECT * FROM performances ORDER BY id DESC", connexion)
    connexion.close()
    return df


def charger_donnees_demo():
    """
    Insère 50 étudiants fictifs dans la base pour les démonstrations.
    Tu peux ensuite les modifier, les supprimer ou en ajouter d'autres.
    """
    import random
    ETUDIANTS_DEMO = [
        ("Mbarga Jean-Pierre",    "Masculin", "Informatique",                "L2", "Analyse de données",      14.5, 15, 85),
        ("Nguema Astrid",         "Féminin",  "Informatique",                "L2", "Analyse de données",      17.0, 22, 95),
        ("Tchamda Boris",         "Masculin", "Informatique",                "L2", "Analyse de données",       9.5,  8, 60),
        ("Kamga Laure",           "Féminin",  "Informatique",                "L2", "Analyse de données",      13.0, 12, 78),
        ("Essono Paul",           "Masculin", "Informatique",                "L2", "Analyse de données",      11.5, 10, 70),
        ("Bikié Carine",          "Féminin",  "Informatique",                "L2", "Analyse de données",      16.5, 20, 92),
        ("Nkoulou Rodrigue",      "Masculin", "Informatique",                "L2", "Analyse de données",       7.0,  5, 45),
        ("Ondoa Mireille",        "Féminin",  "Informatique",                "L2", "Analyse de données",      15.5, 18, 88),
        ("Abanda Christian",      "Masculin", "Informatique",                "L2", "Analyse de données",      12.0, 11, 75),
        ("Fouda Stéphanie",       "Féminin",  "Informatique",                "L2", "Analyse de données",      18.5, 25, 98),
        ("Djoumessi Armel",       "Masculin", "Mathématiques",               "L3", "Algèbre linéaire",        16.0, 20, 90),
        ("Tsanga Inès",           "Féminin",  "Mathématiques",               "L3", "Algèbre linéaire",        19.0, 28,100),
        ("Owona Serge",           "Masculin", "Mathématiques",               "L3", "Algèbre linéaire",        10.0,  9, 65),
        ("Mbassi Flore",          "Féminin",  "Mathématiques",               "L3", "Algèbre linéaire",        14.0, 16, 82),
        ("Bekolo Didier",         "Masculin", "Mathématiques",               "L3", "Algèbre linéaire",         8.5,  7, 55),
        ("Ngo Biyong Sylvie",     "Féminin",  "Mathématiques",               "L3", "Algèbre linéaire",        17.5, 23, 95),
        ("Feudjio Gaëtan",        "Masculin", "Économie-Gestion",            "L1", "Microéconomie",           11.0, 10, 72),
        ("Ateba Sandrine",        "Féminin",  "Économie-Gestion",            "L1", "Microéconomie",           13.5, 14, 80),
        ("Nkoa Joël",             "Masculin", "Économie-Gestion",            "L1", "Microéconomie",            6.5,  4, 40),
        ("Mvondo Pauline",        "Féminin",  "Économie-Gestion",            "L1", "Microéconomie",           15.0, 17, 87),
        ("Biyong Thierry",        "Masculin", "Économie-Gestion",            "L1", "Microéconomie",           10.5,  9, 68),
        ("Essama Rachel",         "Féminin",  "Économie-Gestion",            "L1", "Microéconomie",           12.5, 13, 78),
        ("Nanga Wilfried",        "Masculin", "Physique-Chimie",             "L2", "Mécanique quantique",      9.0,  8, 58),
        ("Mbam Aurelie",          "Féminin",  "Physique-Chimie",             "L2", "Mécanique quantique",     14.0, 15, 83),
        ("Zambo Franck",          "Masculin", "Physique-Chimie",             "L2", "Mécanique quantique",     12.0, 12, 74),
        ("Edo'o Patricia",        "Féminin",  "Physique-Chimie",             "L2", "Mécanique quantique",     16.5, 21, 91),
        ("Ndoumou Kevin",         "Masculin", "Sciences de la Vie",          "L1", "Biologie cellulaire",     13.0, 13, 79),
        ("Olinga Berthe",         "Féminin",  "Sciences de la Vie",          "L1", "Biologie cellulaire",     17.0, 22, 94),
        ("Mekongo Jules",         "Masculin", "Sciences de la Vie",          "L1", "Biologie cellulaire",      8.0,  6, 50),
        ("Ayissi Diane",          "Féminin",  "Sciences de la Vie",          "L1", "Biologie cellulaire",     15.5, 19, 89),
        ("Ndjock Alexis",         "Masculin", "Informatique",                "M1", "Machine Learning",        18.0, 30, 97),
        ("Bebey Christelle",      "Féminin",  "Informatique",                "M1", "Machine Learning",        15.0, 18, 85),
        ("Tchamba Rostand",       "Masculin", "Informatique",                "M1", "Machine Learning",        11.5, 10, 70),
        ("Menguele Ornella",      "Féminin",  "Informatique",                "M1", "Machine Learning",        14.0, 16, 82),
        ("Ekambi Thierry",        "Masculin", "Informatique",                "M1", "Machine Learning",        16.5, 24, 93),
        ("Zanga Alice",           "Féminin",  "Lettres & Sciences Humaines", "L2", "Linguistique",            14.5, 15, 84),
        ("Manga Edouard",         "Masculin", "Lettres & Sciences Humaines", "L2", "Linguistique",            10.0,  9, 66),
        ("Ngo Mboula Cécile",     "Féminin",  "Lettres & Sciences Humaines", "L2", "Linguistique",            16.0, 20, 90),
        ("Bello Simon",           "Masculin", "Lettres & Sciences Humaines", "L2", "Linguistique",             7.5,  5, 48),
        ("Tatchou Vanessa",       "Féminin",  "Économie-Gestion",            "M1", "Économétrie",             17.5, 26, 96),
        ("Eto'o Junior",          "Masculin", "Économie-Gestion",            "M1", "Économétrie",             13.5, 14, 80),
        ("Nkoa Madeleine",        "Féminin",  "Économie-Gestion",            "M1", "Économétrie",             12.0, 11, 73),
        ("Mvele Patrick",         "Masculin", "Économie-Gestion",            "M1", "Économétrie",              9.5,  8, 60),
        ("Ayolo Nadia",           "Féminin",  "Mathématiques",               "M2", "Probabilités avancées",   18.5, 30, 98),
        ("Biwole Ernest",         "Masculin", "Mathématiques",               "M2", "Probabilités avancées",   15.5, 20, 87),
        ("Nkouaga Jeanne",        "Féminin",  "Mathématiques",               "M2", "Probabilités avancées",   14.0, 17, 83),
        ("Essama Rodrigue",       "Masculin", "Informatique",                "L3", "Bases de données",        13.5, 14, 80),
        ("Moukam Ghislaine",      "Féminin",  "Informatique",                "L3", "Bases de données",        16.0, 21, 91),
        ("Onana Christian",       "Masculin", "Informatique",                "L3", "Bases de données",        10.5,  9, 67),
        ("Beng Martine",          "Féminin",  "Informatique",                "L3", "Bases de données",        15.0, 18, 85),
    ]
    connexion = sqlite3.connect(NOM_BDD)
    curseur = connexion.cursor()
    for nom, sexe, filiere, niveau, matiere, note, heures, presence in ETUDIANTS_DEMO:
        date = f"{random.randint(1,28):02d}/{random.randint(1,4):02d}/2025 {random.randint(8,17):02d}:00"
        curseur.execute("""
            INSERT INTO performances
                (nom, filiere, niveau, matiere, note, heures_etude, taux_presence, sexe, date_saisie)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, filiere, niveau, matiere, note, heures, presence, sexe, date))
    connexion.commit()
    connexion.close()


def supprimer_entree(id_ligne):
    """Supprime une ligne de la base selon son identifiant."""
    connexion = sqlite3.connect(NOM_BDD)
    connexion.execute("DELETE FROM performances WHERE id = ?", (id_ligne,))
    connexion.commit()
    connexion.close()


def mention(note):
    """Retourne la mention selon la note sur 20."""
    if note >= 18:  return "Excellent"
    elif note >= 16: return "Très Bien"
    elif note >= 14: return "Bien"
    elif note >= 12: return "Assez Bien"
    elif note >= 10: return "Passable"
    else:            return "Insuffisant"


# ===========================================================
# DÉMARRAGE : Initialise la BDD au lancement de l'app
# ===========================================================
initialiser_bdd()


# ===========================================================
# EN-TÊTE PRINCIPAL (affiché sur toutes les pages)
# ===========================================================
st.markdown("""
<div class="main-header">
    <h1>🎓 EduStat</h1>
    <p>Application de Collecte & Analyse Descriptive des Performances Scolaires</p>
</div>
""", unsafe_allow_html=True)


# ===========================================================
# MENU DE NAVIGATION (barre latérale gauche)
# ===========================================================
st.sidebar.title("📋 Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio("Aller à :", [
    "📝  Saisir des données",
    "📋  Tableau des données",
    "📊  Analyse descriptive",
    "ℹ️  À propos"
])

# Compteur de données dans la sidebar
df_count = lire_donnees()
st.sidebar.markdown("---")
st.sidebar.metric("📦 Données enregistrées", len(df_count))
if len(df_count) > 0:
    st.sidebar.metric("📊 Moyenne générale", f"{df_count['note'].mean():.2f}/20")

# ----------------------------------------------------------
# BOUTON : Charger les données de démonstration
# ----------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧪 Données de démo")
if st.sidebar.button("📥 Charger 50 étudiants démo", use_container_width=True):
    charger_donnees_demo()
    st.sidebar.success("50 étudiants chargés !")
    st.rerun()

if len(df_count) > 0:
    if st.sidebar.button("🗑️ Vider toute la base", use_container_width=True, type="primary"):
        conn_tmp = sqlite3.connect(NOM_BDD)
        conn_tmp.execute("DELETE FROM performances")
        conn_tmp.commit()
        conn_tmp.close()
        st.sidebar.success("Base vidée.")
        st.rerun()


# ===========================================================
# PAGE 1 — FORMULAIRE DE SAISIE
# ===========================================================
if page == "📝  Saisir des données":

    st.header("📝 Formulaire de Saisie")
    st.write("Enregistrez ici les informations de performance d'un étudiant.")

    # st.form = formulaire groupé, soumis en une seule fois
    with st.form("saisie_form", clear_on_submit=True):

        col1, col2 = st.columns(2)   # 2 colonnes côte à côte

        with col1:
            st.subheader("👤 Informations personnelles")
            nom      = st.text_input("Nom complet *", placeholder="Ex: Kouassi Jean")
            sexe     = st.radio("Sexe", ["Masculin", "Féminin"], horizontal=True)
            filiere  = st.selectbox("Filière / Département", [
                "Informatique", "Mathématiques", "Physique-Chimie",
                "Sciences de la Vie", "Économie-Gestion",
                "Lettres & Sciences Humaines", "Droit", "Autre"
            ])
            niveau   = st.selectbox("Niveau d'études", ["L1", "L2", "L3", "M1", "M2", "Doctorat"])

        with col2:
            st.subheader("📚 Informations académiques")
            matiere  = st.text_input("Matière / Module *", placeholder="Ex: Analyse de données")
            note     = st.slider("Note obtenue /20", min_value=0.0, max_value=20.0,
                                 value=10.0, step=0.5, help="Glissez pour sélectionner")
            heures   = st.number_input("Heures d'étude par semaine", min_value=0,
                                       max_value=80, value=10,
                                       help="Temps personnel de travail hebdomadaire")
            presence = st.slider("Taux de présence en cours (%)", 0, 100, 80)

        # Bouton de soumission (prend toute la largeur)
        soumis = st.form_submit_button("💾 Enregistrer les données", use_container_width=True)

    # Traitement après soumission
    if soumis:
        # Validation : les champs obligatoires ne doivent pas être vides
        if nom.strip() == "" or matiere.strip() == "":
            st.error("⚠️ Veuillez renseigner le **nom** et la **matière** (champs marqués *).")
        else:
            inserer_etudiant(nom.strip(), filiere, niveau, matiere.strip(),
                             note, heures, presence, sexe)
            st.success(f"✅ Données de **{nom}** enregistrées ! Mention : **{mention(note)}**")
            st.balloons()   # Animation de ballons 🎈


# ===========================================================
# PAGE 2 — TABLEAU DES DONNÉES
# ===========================================================
elif page == "📋  Tableau des données":

    st.header("📋 Données Collectées")
    df = lire_donnees()

    if df.empty:
        st.info("📭 Aucune donnée enregistrée. Commencez par remplir le formulaire.")

    else:
        st.success(f"✅ **{len(df)}** enregistrement(s) dans la base de données.")

        # ----- Filtres dynamiques -----
        st.subheader("🔍 Filtres")
        c1, c2, c3 = st.columns(3)
        with c1:
            sel_filiere = st.multiselect("Par filière", sorted(df["filiere"].unique()))
        with c2:
            sel_niveau  = st.multiselect("Par niveau",  sorted(df["niveau"].unique()))
        with c3:
            sel_sexe    = st.multiselect("Par sexe",    sorted(df["sexe"].unique()))

        df_f = df.copy()
        if sel_filiere: df_f = df_f[df_f["filiere"].isin(sel_filiere)]
        if sel_niveau:  df_f = df_f[df_f["niveau"].isin(sel_niveau)]
        if sel_sexe:    df_f = df_f[df_f["sexe"].isin(sel_sexe)]

        # Ajoute colonne Mention calculée
        df_f["mention"] = df_f["note"].apply(mention)

        # Affichage du tableau
        st.dataframe(
            df_f[["nom","sexe","filiere","niveau","matiere",
                  "note","mention","heures_etude","taux_presence","date_saisie"]].rename(columns={
                "nom":"Nom", "sexe":"Sexe", "filiere":"Filière", "niveau":"Niveau",
                "matiere":"Matière", "note":"Note/20", "mention":"Mention",
                "heures_etude":"H. Étude/sem", "taux_presence":"Présence %",
                "date_saisie":"Date de saisie"
            }),
            use_container_width=True, hide_index=True
        )

        # ----- Export CSV -----
        csv = df_f.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Exporter en CSV", data=csv,
                           file_name="edustat_donnees.csv", mime="text/csv")

        # ----- Suppression -----
        with st.expander("🗑️ Supprimer une entrée"):
            ids = df["id"].tolist()
            noms = [f"ID {r['id']} — {r['nom']} ({r['matiere']})"
                    for _, r in df.iterrows()]
            choix = st.selectbox("Sélectionner l'entrée à supprimer", noms)
            if st.button("Supprimer", type="primary"):
                id_sup = int(choix.split("—")[0].replace("ID", "").strip())
                supprimer_entree(id_sup)
                st.success("Entrée supprimée. Rechargez la page (F5) pour voir les changements.")


# ===========================================================
# PAGE 3 — ANALYSE DESCRIPTIVE
# ===========================================================
elif page == "📊  Analyse descriptive":

    st.header("📊 Analyse Descriptive des Données")
    df = lire_donnees()

    if len(df) < 3:
        st.warning("⚠️ Ajoutez au moins **3 enregistrements** pour une analyse pertinente.")
        st.stop()   # Arrête l'exécution de cette page ici

    df["mention"] = df["note"].apply(mention)

    # ---- MÉTRIQUES RÉSUMÉES ----
    st.subheader("📌 Indicateurs Clés")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("👥 Étudiants", len(df))
    c2.metric("📊 Moyenne",   f"{df['note'].mean():.2f}/20")
    c3.metric("📈 Médiane",   f"{df['note'].median():.2f}/20")
    c4.metric("🏆 Max",       f"{df['note'].max():.1f}/20")
    c5.metric("📉 Min",       f"{df['note'].min():.1f}/20")

    st.markdow