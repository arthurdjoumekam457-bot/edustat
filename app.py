# =========================================================
# Projet : EduStat
# Cours  : INF232 - Analyse de données
# Sujet  : Analyse des performances académiques
# =========================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
import random

# -------------------------
# CONFIG
# -------------------------
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
    c = conn.cursor()

    c.execute("""
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
    df = pd.read_sql("SELECT * FROM performances ORDER BY id DESC", conn)
    conn.close()
    return df


def delete_data(id):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM performances WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def mention(note):
    if note >= 18:
        return "Excellent"
    elif note >= 16:
        return "Très bien"
    elif note >= 14:
        return "Bien"
    elif note >= 12:
        return "Assez bien"
    elif note >= 10:
        return "Passable"
    else:
        return "Insuffisant"


# -------------------------
# DONNÉES DE TEST (50 étudiants)
# -------------------------
def generer_donnees_test():
    data = [
        ("Mbarga Jean-Pierre","Masculin","Informatique","L2","Analyse",14.5,15,85),
        ("Nguema Astrid","Féminin","Informatique","L2","Analyse",17,22,95),
        ("Tchamda Boris","Masculin","Informatique","L2","Analyse",9.5,8,60),
        ("Kamga Laure","Féminin","Informatique","L2","Analyse",13,12,78),
        ("Essono Paul","Masculin","Informatique","L2","Analyse",11.5,10,70),
        ("Bikié Carine","Féminin","Informatique","L2","Analyse",16.5,20,92),
        ("Nkoulou Rodrigue","Masculin","Informatique","L2","Analyse",7,5,45),
        ("Ondoa Mireille","Féminin","Informatique","L2","Analyse",15.5,18,88),
        ("Abanda Christian","Masculin","Informatique","L2","Analyse",12,11,75),
        ("Fouda Stéphanie","Féminin","Informatique","L2","Analyse",18.5,25,98),

        ("Djoumessi Armel","Masculin","Maths","L3","Algèbre",16,20,90),
        ("Tsanga Inès","Féminin","Maths","L3","Algèbre",19,28,100),
        ("Owona Serge","Masculin","Maths","L3","Algèbre",10,9,65),
        ("Mbassi Flore","Féminin","Maths","L3","Algèbre",14,16,82),
        ("Bekolo Didier","Masculin","Maths","L3","Algèbre",8.5,7,55),

        ("Feudjio Gaëtan","Masculin","Economie","L1","Micro",11,10,72),
        ("Ateba Sandrine","Féminin","Economie","L1","Micro",13.5,14,80),
        ("Nkoa Joël","Masculin","Economie","L1","Micro",6.5,4,40),
        ("Mvondo Pauline","Féminin","Economie","L1","Micro",15,17,87),
        ("Biyong Thierry","Masculin","Economie","L1","Micro",10.5,9,68),
    ]

    for d in data:
        date = f"{random.randint(1,28):02d}/04/2025 {random.randint(8,17):02d}:00"
        add_data(d[0], d[2], d[3], d[4], d[5], d[6], d[7], d[1])


# -------------------------
# INITIALISATION
# -------------------------
init_db()

# -------------------------
# INTERFACE
# -------------------------
st.title("🎓 EduStat")
st.write("Application simple pour suivre les performances des étudiants.")

menu = st.sidebar.selectbox("Menu", [
    "Saisie",
    "Données",
    "Analyse",
    "A propos"
])

df = load_data()

# -------------------------
# PAGE SAISIE
# -------------------------
if menu == "Saisie":

    st.header("Ajouter un étudiant")

    nom = st.text_input("Nom")
    sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])
    filiere = st.selectbox("Filière", ["Informatique", "Maths", "Economie"])
    niveau = st.selectbox("Niveau", ["L1","L2","L3","M1","M2"])

    matiere = st.text_input("Matière")
    note = st.slider("Note", 0.0, 20.0, 10.0)
    heures = st.number_input("Heures d'étude", 0, 50, 10)
    presence = st.slider("Présence (%)", 0, 100, 80)

    if st.button("Enregistrer"):
        if nom == "" or matiere == "":
            st.warning("Remplir les champs")
        else:
            add_data(nom, filiere, niveau, matiere, note, heures, presence, sexe)
            st.success("Ajout effectué")


# -------------------------
# PAGE DONNÉES
# -------------------------
elif menu == "Données":

    st.header("Liste")

    if df.empty:
        st.info("Aucune donnée")
    else:
        df["mention"] = df["note"].apply(mention)
        st.dataframe(df)

        if st.button("Générer données test"):
            generer_donnees_test()
            st.success("Données ajoutées")

        id_sup = st.number_input("ID à supprimer", 0, 1000, 0)
        if st.button("Supprimer"):
            delete_data(id_sup)
            st.success("Supprimé")


# -------------------------
# PAGE ANALYSE
# -------------------------
elif menu == "Analyse":

    st.header("Analyse")

    if len(df) < 3:
        st.warning("Pas assez de données")
    else:
        st.metric("Moyenne", round(df["note"].mean(), 2))
        st.metric("Max", df["note"].max())
        st.metric("Min", df["note"].min())

        fig = px.histogram(df, x="note")
        st.plotly_chart(fig)

        fig2 = px.scatter(df, x="heures", y="note")
        st.plotly_chart(fig2)


# -------------------------
# PAGE A PROPOS
# -------------------------
else:
    st.header("A propos")
    st.write("Projet réalisé dans le cadre du cours INF232.")