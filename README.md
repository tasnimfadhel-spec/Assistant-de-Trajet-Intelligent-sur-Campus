# 🎓 Assistant de Trajet Intelligent sur Campus

## 📌 Description

Assistant de navigation intelligent permettant de trouver un chemin entre deux lieux d'un campus universitaire.

Ce projet compare trois algorithmes de recherche de chemin : **BFS, Dijkstra et A\***. L'application utilise Streamlit pour proposer une interface interactive.

## ✨ Fonctionnalités

- Sélection du point de départ et de la destination.
- Recherche de chemin avec BFS, Dijkstra et A*.
- Calcul de la distance totale en mètres.
- Comparaison des algorithmes : coût, nœuds explorés et temps d'exécution.
- Visualisation du graphe du campus.
- Gestion des zones fermées.
- Interface web avec Streamlit.

## 🛠️ Technologies utilisées

- Python
- Streamlit
- NetworkX
- Matplotlib
- NumPy
- Pandas

## 📂 Structure du projet

```text
AssistantCampus/
├── path_readmap.py
├── README.md
└── requirements.txt
```

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone URL_DE_VOTRE_DEPOT
cd AssistantCampus
```

### 2. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

### 3. Lancer l'application

```bash
python -m streamlit run path_readmap.py
```

L'application sera accessible dans le navigateur, généralement à l'adresse `http://localhost:8501`.

## 🧠 Algorithmes

- **BFS (Breadth-First Search)** : recherche un chemin avec le moins d'arêtes, sans optimiser directement la distance.
- **Dijkstra** : recherche le chemin de coût minimal en tenant compte des distances.
- **A\*** : utilise le coût parcouru et une heuristique pour guider la recherche.

## 🎯 Objectif pédagogique

Comprendre, implémenter et comparer différents algorithmes de recherche de chemin dans un graphe pondéré.

## 👩‍💻 Auteur

Projet académique — Assistant de Trajet Intelligent sur Campus.
