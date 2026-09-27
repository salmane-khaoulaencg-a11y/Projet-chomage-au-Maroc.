"""
Analyse du chômage au Maroc - Résultats HCP 2025
==================================================
Ce script importe les données extraites du rapport du Haut-Commissariat au Plan
"Activité, Emploi et Chômage - Résultats annuels 2025" et génère 4 graphiques
illustrant pourquoi le taux de chômage reste structurellement élevé / augmente
pour certaines catégories de la population, malgré une quasi-stagnation au
niveau national.

Source des données : Haut-Commissariat au Plan (HCP), Maroc
https://www.hcp.ma  (Division des Enquêtes sur l'Emploi, Direction de la Statistique)

Prérequis : pandas, matplotlib
    pip install pandas matplotlib
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# 0. Configuration des chemins
# ------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUT_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams["figure.dpi"] = 110
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titleweight"] = "bold"


# ------------------------------------------------------------------
# 1. Graphique : Taux de chômage par catégorie, 2024 vs 2025
# ------------------------------------------------------------------
def graphique_categories():
    df = pd.read_csv(os.path.join(DATA_DIR, "taux_chomage_categories_2024_2025.csv"))

    x = range(len(df))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar([i - width / 2 for i in x], df["taux_2024"], width, label="2024", color="#8896a6")
    ax.bar([i + width / 2 for i in x], df["taux_2025"], width, label="2025", color="#c0392b")

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["categorie"], rotation=35, ha="right")
    ax.set_ylabel("Taux de chômage (%)")
    ax.set_title("Taux de chômage par catégorie - Maroc, 2024 vs 2025")
    ax.legend()

    # Étiquettes de valeurs
    for i in x:
        ax.text(i - width / 2, df["taux_2024"][i] + 0.3, f"{df['taux_2024'][i]}", ha="center", fontsize=8)
        ax.text(i + width / 2, df["taux_2025"][i] + 0.3, f"{df['taux_2025'][i]}", ha="center", fontsize=8)

    fig.tight_layout()
    out_path = os.path.join(OUT_DIR, "1_chomage_categories_2024_2025.png")
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[OK] Graphique généré : {out_path}")


# ------------------------------------------------------------------
# 2. Graphique : Évolution trimestrielle du chômage en 2025
# ------------------------------------------------------------------
def graphique_trimestriel():
    df = pd.read_csv(os.path.join(DATA_DIR, "taux_chomage_trimestriel_2025.csv"))
    df_trimestres = df[df["periode"] != "Annee_2025"]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(df_trimestres["periode"], df_trimestres["taux_chomage_national"],
            marker="o", linewidth=2, color="#c0392b")

    for i, row in df_trimestres.iterrows():
        ax.annotate(f"{row['taux_chomage_national']}%",
                    (row["periode"], row["taux_chomage_national"]),
                    textcoords="offset points", xytext=(0, 8), ha="center")

    ax.set_ylabel("Taux de chômage national (%)")
    ax.set_title("Évolution trimestrielle du taux de chômage - Maroc, 2025")
    ax.set_ylim(11, 14)
    fig.tight_layout()

    out_path = os.path.join(OUT_DIR, "2_chomage_trimestriel_2025.png")
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[OK] Graphique généré : {out_path}")


# ------------------------------------------------------------------
# 3. Graphique : Taux de chômage par région, 2025
# ------------------------------------------------------------------
def graphique_regions():
    df = pd.read_csv(os.path.join(DATA_DIR, "taux_chomage_regions_2025.csv"))
    df = df.sort_values("taux_chomage_pct", ascending=True)

    colors = ["#c0392b" if r == "National" else "#2e6da4" for r in df["region"]]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(df["region"], df["taux_chomage_pct"], color=colors)

    for i, (val, region) in enumerate(zip(df["taux_chomage_pct"], df["region"])):
        ax.text(val + 0.3, i, f"{val}%", va="center", fontsize=8)

    ax.set_xlabel("Taux de chômage (%)")
    ax.set_title("Taux de chômage par région - Maroc, 2025")
    fig.tight_layout()

    out_path = os.path.join(OUT_DIR, "3_chomage_regions_2025.png")
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[OK] Graphique généré : {out_path}")


# ------------------------------------------------------------------
# 4. Graphique : Taux de chômage selon l'âge et le diplôme, 2025
# ------------------------------------------------------------------
def graphique_diplome_age():
    df = pd.read_csv(os.path.join(DATA_DIR, "taux_chomage_diplome_age_2025.csv"))
    df = df.set_index("diplome")

    fig, ax = plt.subplots(figsize=(9, 6))
    df.T.plot(kind="bar", ax=ax, color=["#8896a6", "#2e6da4", "#c0392b"])

    ax.set_ylabel("Taux de chômage (%)")
    ax.set_xlabel("Tranche d'âge")
    ax.set_title("Taux de chômage selon l'âge et le niveau de diplôme - Maroc, 2025")
    ax.legend(title="Diplôme")
    plt.xticks(rotation=0)
    fig.tight_layout()

    out_path = os.path.join(OUT_DIR, "4_chomage_diplome_age_2025.png")
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[OK] Graphique généré : {out_path}")


# ------------------------------------------------------------------
# Point d'entrée
# ------------------------------------------------------------------
if __name__ == "__main__":
    graphique_categories()
    graphique_trimestriel()
    graphique_regions()
    graphique_diplome_age()
    print("\nTous les graphiques ont été générés dans le dossier 'figures/'.")
