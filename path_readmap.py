"""
=============================================================
  ASSISTANT DE TRAJET INTELLIGENT SUR CAMPUS
  Algorithmes : BFS, Dijkstra, A*
  Visualisation : NetworkX + Matplotlib
  Compatible : Google Colab / Jupyter Notebook / Script Python
=============================================================
"""

# ─── IMPORTATIONS ──────────────────────────────────────────
import heapq
import math
import time
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

# ══════════════════════════════════════════════════════════════════
# 1.  MODÉLISATION DU CAMPUS (graphe pondéré non orienté)
# ══════════════════════════════════════════════════════════════════

# Coordonnées 2D de chaque lieu (utilisées comme heuristique pour A*)
POSITIONS = {
    "Entrée Principale":   (0.0, 5.0),
    "Accueil / Sécurité":  (1.0, 5.0),
    "Administration":      (1.0, 7.0),
    "Amphithéâtre A":      (3.0, 7.5),
    "Amphithéâtre B":      (3.0, 5.5),
    "Bibliothèque":        (5.0, 8.0),
    "Cafétéria":           (5.0, 5.0),
    "Laboratoire Info":    (7.0, 7.0),
    "Laboratoire Sciences":(7.0, 4.5),
    "Résidence":           (9.0, 8.0),
    "Salle de Sport":      (9.0, 5.5),
    "Parking":             (9.0, 3.0),
    "Jardin / Parc":       (5.0, 2.5),
    "Infirmerie":          (2.5, 3.0),
}

# Arêtes : (lieu_A, lieu_B, distance_en_metres)
ARETES = [
    ("Entrée Principale",    "Accueil / Sécurité",   80),
    ("Accueil / Sécurité",   "Administration",       120),
    ("Accueil / Sécurité",   "Amphithéâtre B",       200),
    ("Accueil / Sécurité",   "Infirmerie",           180),
    ("Administration",       "Amphithéâtre A",       150),
    ("Administration",       "Amphithéâtre B",       130),
    ("Amphithéâtre A",       "Bibliothèque",         200),
    ("Amphithéâtre A",       "Amphithéâtre B",       100),
    ("Amphithéâtre B",       "Cafétéria",            160),
    ("Amphithéâtre B",       "Laboratoire Info",     300),
    ("Bibliothèque",         "Laboratoire Info",     180),
    ("Bibliothèque",         "Résidence",            250),
    ("Cafétéria",            "Laboratoire Sciences", 200),
    ("Cafétéria",            "Jardin / Parc",        150),
    ("Laboratoire Info",     "Laboratoire Sciences", 220),
    ("Laboratoire Info",     "Résidence",            200),
    ("Laboratoire Sciences", "Salle de Sport",       180),
    ("Laboratoire Sciences", "Parking",              200),
    ("Résidence",            "Salle de Sport",       150),
    ("Salle de Sport",       "Parking",              130),
    ("Jardin / Parc",        "Infirmerie",           200),
    ("Jardin / Parc",        "Parking",              300),
]

# ══════════════════════════════════════════════════════════════════
# 2.  CONSTRUCTION DU GRAPHE NetworkX
# ══════════════════════════════════════════════════════════════════

def construire_graphe(zones_fermees=None):
    """
    Construit le graphe du campus.
    zones_fermees : liste de nœuds à exclure (option 'zone fermée')
    """
    if zones_fermees is None:
        zones_fermees = []

    G = nx.Graph()

    # Ajout des nœuds avec leurs positions
    for lieu, pos in POSITIONS.items():
        if lieu not in zones_fermees:
            G.add_node(lieu, pos=pos)

    # Ajout des arêtes (on ignore celles qui touchent une zone fermée)
    for (a, b, dist) in ARETES:
        if a not in zones_fermees and b not in zones_fermees:
            G.add_edge(a, b, weight=dist)

    return G


# ══════════════════════════════════════════════════════════════════
# 3.  ALGORITHME BFS  (Breadth-First Search)
# ══════════════════════════════════════════════════════════════════

def bfs(G, depart, arrivee):
    """
    BFS : recherche en largeur — trouve le chemin avec le moins de sauts,
    SANS tenir compte des distances/poids.

    Retourne : (chemin, coût_total, nb_noeuds_explorés)
    """
    if depart not in G or arrivee not in G:
        return None, float('inf'), 0

    file = deque([(depart, [depart])])     # (nœud_courant, chemin_parcouru)
    visites = {depart}
    expansions = 0

    while file:
        noeud, chemin = file.popleft()
        expansions += 1

        if noeud == arrivee:
            # Calcul du coût réel (somme des poids le long du chemin trouvé)
            cout = sum(G[chemin[i]][chemin[i+1]]['weight']
                       for i in range(len(chemin) - 1))
            return chemin, cout, expansions

        for voisin in G.neighbors(noeud):
            if voisin not in visites:
                visites.add(voisin)
                file.append((voisin, chemin + [voisin]))

    return None, float('inf'), expansions   # Aucun chemin trouvé


# ══════════════════════════════════════════════════════════════════
# 4.  ALGORITHME DIJKSTRA
# ══════════════════════════════════════════════════════════════════

def dijkstra(G, depart, arrivee):
    """
    Dijkstra : trouve le chemin le plus court en tenant compte des poids.

    Retourne : (chemin, coût_total, nb_noeuds_explorés)
    """
    if depart not in G or arrivee not in G:
        return None, float('inf'), 0

    # File de priorité : (coût_cumulé, nœud, chemin)
    file = [(0, depart, [depart])]
    visites = {}
    expansions = 0

    while file:
        cout, noeud, chemin = heapq.heappop(file)
        expansions += 1

        if noeud in visites:
            continue
        visites[noeud] = cout

        if noeud == arrivee:
            return chemin, cout, expansions

        for voisin, data in G[noeud].items():
            if voisin not in visites:
                nouveau_cout = cout + data['weight']
                heapq.heappush(file, (nouveau_cout, voisin, chemin + [voisin]))

    return None, float('inf'), expansions


# ══════════════════════════════════════════════════════════════════
# 5.  ALGORITHME A*  (avec heuristique distance euclidienne)
# ══════════════════════════════════════════════════════════════════

def heuristique_euclidienne(noeud, arrivee):
    """
    Heuristique admissible : distance euclidienne entre deux nœuds
    (basée sur leurs coordonnées 2D × un facteur d'échelle ~30 m/unité).
    """
    x1, y1 = POSITIONS[noeud]
    x2, y2 = POSITIONS[arrivee]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 30


def a_star(G, depart, arrivee):
    """
    A* : combine Dijkstra et une heuristique pour explorer moins de nœuds.

    f(n) = g(n) + h(n)
      g(n) : coût réel depuis le départ
      h(n) : estimation (heuristique euclidienne) jusqu'à l'arrivée

    Retourne : (chemin, coût_total, nb_noeuds_explorés)
    """
    if depart not in G or arrivee not in G:
        return None, float('inf'), 0

    # File de priorité : (f, g, nœud, chemin)
    h0 = heuristique_euclidienne(depart, arrivee)
    file = [(h0, 0, depart, [depart])]
    visites = {}
    expansions = 0

    while file:
        f, g, noeud, chemin = heapq.heappop(file)
        expansions += 1

        if noeud in visites:
            continue
        visites[noeud] = g

        if noeud == arrivee:
            return chemin, g, expansions

        for voisin, data in G[noeud].items():
            if voisin not in visites:
                g_new = g + data['weight']
                h_new = heuristique_euclidienne(voisin, arrivee)
                f_new = g_new + h_new
                heapq.heappush(file, (f_new, g_new, voisin, chemin + [voisin]))

    return None, float('inf'), expansions



import streamlit as st
import pandas as pd

st.set_page_config(page_title="Assistant de trajet campus", page_icon="🎓", layout="wide")
st.title("🎓 Assistant de Trajet Intelligent — Campus")
st.write("Comparez BFS, Dijkstra et A* pour trouver un trajet entre deux lieux du campus.")

with st.sidebar:
    st.header("⚙️ Paramètres du trajet")
    zones_fermees = st.multiselect(
        "Zones fermées (facultatif)",
        options=list(POSITIONS.keys()),
        default=[]
    )

G = construire_graphe(zones_fermees=zones_fermees)
lieux_disponibles = list(G.nodes())

if len(lieux_disponibles) < 2:
    st.error("Il faut au moins deux lieux ouverts pour calculer un trajet.")
    st.stop()

with st.sidebar:
    depart = st.selectbox("📍 Départ", lieux_disponibles, index=0)
    arrivee_options = [lieu for lieu in lieux_disponibles if lieu != depart]
    arrivee = st.selectbox("🏁 Arrivée", arrivee_options, index=0)
    algo_choisi = st.selectbox("Algorithme à mettre en évidence", ["Dijkstra", "A*", "BFS"])
    comparer = st.checkbox("Comparer les trois algorithmes", value=True)

algorithmes = {"BFS": bfs, "Dijkstra": dijkstra, "A*": a_star}
resultats = {}
for nom, fonction in algorithmes.items():
    debut_temps = time.perf_counter()
    chemin, cout, expansions = fonction(G, depart, arrivee)
    duree_ms = (time.perf_counter() - debut_temps) * 1000
    resultats[nom] = (chemin, cout, expansions, duree_ms)

# Résumé du trajet choisi
chemin, cout, expansions, duree_ms = resultats[algo_choisi]
st.subheader(f"Résultat — {algo_choisi}")
if chemin:
    c1, c2, c3 = st.columns(3)
    c1.metric("Distance du trajet", f"{cout} m")
    c2.metric("Nœuds explorés", expansions)
    c3.metric("Temps d'exécution", f"{duree_ms:.3f} ms")
    st.success(" → ".join(chemin))
else:
    st.error("Aucun chemin trouvé entre ces deux lieux avec les zones fermées choisies.")

# Tableau comparatif
if comparer:
    st.subheader("📊 Comparaison des algorithmes")
    lignes = []
    for nom, (chemin_i, cout_i, expansions_i, duree_i) in resultats.items():
        lignes.append({
            "Algorithme": nom,
            "Chemin": " → ".join(chemin_i) if chemin_i else "Aucun chemin",
            "Nombre de lieux dans le chemin": len(chemin_i) if chemin_i else 0,
            "Coût (m)": cout_i if chemin_i else None,
            "Nœuds explorés": expansions_i,
            "Durée (ms)": round(duree_i, 3),
        })
    st.dataframe(pd.DataFrame(lignes), use_container_width=True, hide_index=True)
    st.caption("BFS minimise le nombre de sauts, sans optimiser les distances. Dijkstra et A* tiennent compte des distances.")

# Graphe : mettre en évidence le chemin de l'algorithme choisi
st.subheader("🗺️ Carte du campus")
pos = nx.get_node_attributes(G, "pos")
fig, ax = plt.subplots(figsize=(12, 7))
chemin_set = set()
if chemin:
    for i in range(len(chemin) - 1):
        chemin_set.add((chemin[i], chemin[i + 1]))
        chemin_set.add((chemin[i + 1], chemin[i]))

node_colors = []
for n in G.nodes():
    if n == depart:
        node_colors.append("#F39C12")
    elif n == arrivee:
        node_colors.append("#9B59B6")
    elif chemin and n in chemin:
        node_colors.append("#3498DB")
    else:
        node_colors.append("#BDC3C7")
edge_colors = ["#3498DB" if (u, v) in chemin_set else "#D5D8DC" for u, v in G.edges()]
edge_widths = [4 if (u, v) in chemin_set else 1 for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=edge_widths, alpha=0.9)
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=850)
# Les labels et distances sont affichés sur le graphe.
nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight="bold")
nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=nx.get_edge_attributes(G, "weight"), font_size=7)
ax.set_title(f"{algo_choisi} : {depart} → {arrivee}")
ax.axis("off")
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

with st.expander("Voir les lieux et les connexions du graphe"):
    st.write(f"**Lieux ouverts :** {G.number_of_nodes()} — **Connexions :** {G.number_of_edges()}")
    st.dataframe(pd.DataFrame([
        {"Lieu A": u, "Lieu B": v, "Distance (m)": d["weight"]}
        for u, v, d in G.edges(data=True)
    ]), use_container_width=True, hide_index=True)
