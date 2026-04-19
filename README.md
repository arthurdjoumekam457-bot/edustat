# 🎓 EduStat — Application de Collecte & Analyse Scolaire

Application web de collecte et d'analyse descriptive des performances académiques.  
Développée dans le cadre du cours **INF 232 EC2 — Analyse de données**.

---

## 📁 Structure du projet

```
edustat/
├── app.py            ← Application principale (interface + base de données + graphiques)
├── seed_data.py      ← Script optionnel pour pré-remplir la base avec 50 étudiants fictifs
├── requirements.txt  ← Bibliothèques Python à installer
└── README.md         ← Ce fichier
```

---

## 📄 Rôle de chaque fichier

### `app.py`
C'est le **cœur du projet**. Il contient :
- L'interface web (formulaire, tableau, graphiques)
- La connexion à la base de données SQLite
- Toutes les analyses descriptives
- Le bouton pour charger les données de démonstration

### `seed_data.py`
Script **optionnel** qui insère 50 faux étudiants dans la base pour que
l'application soit présentable dès le premier lancement.  
> Sur Streamlit Cloud, ce fichier est inutile car un bouton dans l'application fait exactement la même chose.

### `requirements.txt`
Liste les bibliothèques Python nécessaires. Streamlit Cloud lit ce fichier
automatiquement pour tout installer avant de lancer l'app.

### `README.md`
Ce guide.

---

## 🚀 Déploiement en ligne (lien cliquable gratuit)

### Étape 1 — Créer un compte GitHub
1. Aller sur [https://github.com](https://github.com)
2. Cliquer sur **Sign up**
3. Créer un compte et vérifier l'adresse email

### Étape 2 — Créer un dépôt
1. Cliquer sur le **+** en haut à droite → **New repository**
2. Nom : `edustat`
3. Visibilité : **Public** ✅ (obligatoire)
4. Cliquer sur **Create repository**

### Étape 3 — Uploader les fichiers
Dans le dépôt vide, cliquer sur **uploading an existing file** puis glisser-déposer les 4 fichiers :
- `app.py`
- `seed_data.py`
- `requirements.txt`
- `README.md`

Écrire un message de commit (ex: `Premier commit`) puis cliquer sur **Commit changes**.

### Étape 4 — Déployer sur Streamlit Community Cloud
1. Aller sur [https://share.streamlit.io](https://share.streamlit.io)
2. Cliquer sur **Sign in with GitHub**
3. Cliquer sur **New app**
4. Remplir le formulaire :
   - **Repository** : `votre-pseudo/edustat`
   - **Branch** : `main`
   - **Main file path** : `app.py`
5. Cliquer sur **Deploy!**

⏳ Attendre 2 à 3 minutes...

### Étape 5 — Récupérer le lien
Une fois déployé, vous obtenez un lien de la forme :
```
https://votre-pseudo-edustat-XXXXX.streamlit.app
```
✅ C'est ce lien que vous envoyez à votre professeur.

---

## 📥 Charger les données de démonstration

Au premier lancement, la base est vide. Pour la remplir avec 50 étudiants fictifs :

**Dans l'application** (barre latérale gauche) :
```
🧪 Données de démo
[ 📥 Charger 50 étudiants démo ]  ←  cliquer ce bouton
```

Les données apparaissent immédiatement. Vous pouvez ensuite les modifier
ou les supprimer depuis la page **📋 Tableau des données**.

> `seed_data.py` fait la même chose mais depuis le terminal — utile uniquement
> si vous testez l'application sur votre propre ordinateur.

---

## 💻 Test en local (sur votre ordinateur)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. (Optionnel) Pré-remplir la base depuis le terminal
python seed_data.py

# 3. Lancer l'application
streamlit run app.py
```

L'application s'ouvre automatiquement à l'adresse : `http://localhost:8501`

---

## 📊 Pages de l'application

| Page | Contenu |
|------|---------|
| 📝 Saisir des données | Formulaire d'enregistrement d'un étudiant |
| 📋 Tableau des données | Visualisation, filtres et export CSV |
| 📊 Analyse descriptive | Statistiques + 6 graphiques interactifs |
| ℹ️ À propos | Description du projet et technologies |

---

## 🔬 Analyses disponibles

- Statistiques descriptives (moyenne, médiane, écart-type, min, max, quartiles)
- Distribution des notes — histogramme
- Répartition des mentions — diagramme en barres
- Performance moyenne par filière — barres horizontales
- Répartition Hommes / Femmes — camembert
- Corrélation heures d'étude ↔ notes — nuage de points + droite de régression
- Corrélation taux de présence ↔ notes — nuage de points + droite de régression
- Comparaison des performances par niveau — tableau synthétique

---

## 🛠️ Technologies

| Outil | Rôle |
|-------|------|
| Python | Langage de programmation principal |
| Streamlit | Création de l'interface web |
| SQLite | Base de données (aucune installation requise) |
| Pandas | Manipulation et analyse des données |
| Plotly | Graphiques interactifs |

---

*INF 232 EC2 — Analyse de données*
