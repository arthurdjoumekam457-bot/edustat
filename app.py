# =========================================================
# Projet : EduStat
# Analyse des performances académiques
# =========================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime
import random

st.set_page_config(page_title="EduStat", page_icon="🎓", layout="wide")

DB = "edustat.db"

# -------------------------
# BASE DE DONNÉES
# -------------------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS performances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        filiere TEXT,
        niveau TEXT,
        matiere TEXT,
        note REAL,
        heures REAL,
        presence REAL,
        sexe TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_data(nom, filiere, niveau, matiere, note, heures, presence, sexe):
    conn = sqlite3.connect(DB)
    conn.execute("""
    INSERT INTO performances 
    (nom, filiere, niveau, matiere, note, heures, presence, sexe, date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nom, filiere, niveau, matiere, note,
        heures, presence, sexe,
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ))
    conn.commit()
    conn.close()


def load_data():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM performances", conn)
    conn.close()
    return df


def mention(note):
    if note >= 18: return "Excellent"
    elif note >= 16: return "Très bien"
    elif note >= 14: return "Bien"
    elif note >= 12: return "Assez bien"
    elif note >= 10: return "Passable"
    else: return "Insuffisant"


# -------------------------
# DONNÉES TEST
# -------------------------
def generer_donnees_test():
    noms = ["Jean", "Marie", "Paul", "Alice", "Kevin", "Nadia", "Serge", "Linda"]
    filieres = ["Informatique", "Maths", "Economie"]

    for _ in range(50):
        add_data(
            random.choice(noms),
            random.choice(filieres),
            random.choice(["L1","L2","L3","M1"]),
            "Analyse",
            random.uniform(5, 19),
            random.randint(5, 25),
            random.randint(50, 100),
            random.choice(["Masculin","Féminin"])
        )


# -------------------------
# INIT
# -------------------------
init_db()

st.title("🎓 EduStat")
menu = st.sidebar.selectbox("Menu", ["Saisie", "Données", "Analyse"])

df = load_data()

# correction compatibilité
if "heures_etude" in df.columns:
    df = df.rename(columns={"heures_etude": "heures"})

# nettoyage
if not df.empty:
    df["note"] = pd.to_numeric(df["note"], errors="coerce")
    df["heures"] = pd.to_numeric(df["heures"], errors="coerce")
    df["mention"] = df["note"].apply(mention)


# -------------------------
# PAGE SAISIE
# -------------------------
if menu == "Saisie":

    st.header("Ajouter un étudiant")

    nom = st.text_input("Nom")
    sexe = st.selectbox("Sexe", ["Masculin","Féminin"])
    filiere = st.selectbox("Filière", ["Informatique","Maths","Economie"])
    niveau = st.selectbox("Niveau", ["L1","L2","L3","M1"])

    matiere = st.text_input("Matière")
    note = st.slider("Note", 0.0, 20.0, 10.0)
    heures = st.number_input("Heures d'étude", 0, 50, 10)
    presence = st.slider("Présence", 0, 100, 80)

    if st.button("Ajouter"):
        add_data(nom, filiere, niveau, matiere, note, heures, presence, sexe)
        st.success("Ajout réussi")


# -------------------------
# PAGE DONNÉES
# -------------------------
elif menu == "Données":

    st.header("Données")

    if df.empty:
        st.warning("Aucune donnée")
    else:
        st.dataframe(df)

    if st.button("Générer données test"):
        generer_donnees_test()
        st.success("Données générées")


# -------------------------
# PAGE ANALYSE
# -------------------------
else:

    st.header("Analyse avancée")

    if len(df) < 5:
        st.warning("Pas assez de données")
    else:

        # indicateurs
        col1, col2, col3 = st.columns(3)
        col1.metric("Moyenne", round(df["note"].mean(),2))
        col2.metric("Max", df["note"].max())
        col3.metric("Min", df["note"].min())

        # Histogramme
        st.subheader("Distribution des notes")
        fig1 = px.histogram(df, x="note", nbins=10)
        st.plotly_chart(fig1)

        # Scatter
        st.subheader("Relation heures vs note")
        fig2 = px.scatter(df, x="heures", y="note", color="filiere")
        st.plotly_chart(fig2)

        # Boxplot
        st.subheader("Comparaison des filières")
        fig3 = px.box(df, x="filiere", y="note", color="filiere")
        st.plotly_chart(fig3)

        # Moyenne par filière
        st.subheader("Moyenne par filière")
        moy = df.groupby("filiere")["note"].mean().reset_index()
        fig4 = px.bar(moy, x="filiere", y="note")
        st.plotly_chart(fig4)

        # Heatmap corrélation
        st.subheader("Corrélation")
        corr = df[["note","heures","presence"]].corr()

        fig5 = ff.create_annotated_heatmap(
            z=corr.values,
            x=list(corr.columns),
            y=list(corr.columns),
            annotation_text=corr.round(2).values,
            showscale=True
        )
        st.plotly_chart(fig5)