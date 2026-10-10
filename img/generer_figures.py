"""Génère les schémas du polycopié (formats SVG pour le web et PDF pour LaTeX).

Usage (depuis la racine du livre) :

    python img/generer_figures.py

Chaque figure est dessinée « à la main » avec matplotlib : les unités des axes
sont des pouces, ce qui permet de garder des tailles de texte cohérentes d'une
figure à l'autre.
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon  # noqa: E402

DOSSIER = os.path.dirname(os.path.abspath(__file__))

BLEU, BLEU_CL = "#2E6DB4", "#DCE8F7"
ORANGE, ORANGE_CL = "#C8641A", "#FBE6D3"
VERT, VERT_CL = "#23875E", "#D7F0E5"
GRIS, GRIS_CL = "#4B5260", "#EEF0F3"
ROUGE, ROUGE_CL = "#B83227", "#F8DEDA"
VIOLET, VIOLET_CL = "#6A4C93", "#E9E1F4"
MONO = "DejaVu Sans Mono"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "svg.fonttype": "path"})


# --------------------------------------------------------------------------
# Petits outils de dessin
# --------------------------------------------------------------------------
def figure(largeur, hauteur):
    fig, ax = plt.subplots(figsize=(largeur, hauteur))
    ax.set_xlim(0, largeur)
    ax.set_ylim(0, hauteur)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def boite(ax, x, y, l, h, texte="", fc=BLEU_CL, ec=BLEU, taille=11, mono=False,
          rayon=0.06, couleur_texte="black", gras=False, lw=1.5, ls="-"):
    """Boîte de coin inférieur gauche (x, y), de largeur l et hauteur h."""
    p = FancyBboxPatch((x, y), l, h, boxstyle=f"round,pad=0,rounding_size={rayon}",
                       fc=fc, ec=ec, lw=lw, ls=ls)
    ax.add_patch(p)
    if texte:
        ax.text(x + l / 2, y + h / 2, texte, ha="center", va="center",
                fontsize=taille, family=MONO if mono else None,
                color=couleur_texte, weight="bold" if gras else "normal")
    return p


def fleche(ax, depart, arrivee, couleur=GRIS, lw=1.6, style="-|>", courbure=0.0,
           ls="-", ms=14):
    a = FancyArrowPatch(depart, arrivee, arrowstyle=style, mutation_scale=ms,
                        color=couleur, lw=lw, ls=ls,
                        connectionstyle=f"arc3,rad={courbure}",
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


def texte(ax, x, y, s, taille=11, mono=False, couleur="black", ha="center",
          va="center", gras=False, italique=False):
    ax.text(x, y, s, fontsize=taille, family=MONO if mono else None,
            color=couleur, ha=ha, va=va, weight="bold" if gras else "normal",
            style="italic" if italique else "normal")


def losange(ax, cx, cy, l, h, s, fc=ORANGE_CL, ec=ORANGE, taille=11):
    pts = [(cx, cy + h / 2), (cx + l / 2, cy), (cx, cy - h / 2), (cx - l / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=1.5))
    texte(ax, cx, cy, s, taille=taille, mono=True)


def sauver(fig, nom):
    for ext in ("svg", "pdf"):
        fig.savefig(os.path.join(DOSSIER, f"{nom}.{ext}"), bbox_inches="tight",
                    pad_inches=0.06)
    if "--png" in sys.argv:  # aperçu pour relecture
        fig.savefig(os.path.join(DOSSIER, f"{nom}.png"), bbox_inches="tight",
                    pad_inches=0.06, dpi=110)
    plt.close(fig)


def cases(ax, x, y, valeurs, l=0.75, h=0.55, fc=BLEU_CL, ec=BLEU, taille=12,
          surlignes=(), fc_sur=ORANGE_CL, ec_sur=ORANGE):
    """Dessine une rangée de cases contiguës (une liste) ; renvoie les centres x."""
    centres = []
    for i, v in enumerate(valeurs):
        sur = i in surlignes
        boite(ax, x + i * l, y, l, h, v, fc=fc_sur if sur else fc,
              ec=ec_sur if sur else ec, taille=taille, mono=True, rayon=0.0)
        centres.append(x + i * l + l / 2)
    return centres


# --------------------------------------------------------------------------
# Chapitre 1 : variables
# --------------------------------------------------------------------------
def fig_variables():
    fig, ax = figure(7.2, 2.3)
    donnees = [("age", "19", "int"), ("taille", "1.72", "float"),
               ("prenom", '"Aude"', "str"), ("inscrite", "True", "bool")]
    for i, (nom, val, typ) in enumerate(donnees):
        x = 0.2 + i * 1.78
        texte(ax, x + 0.7, 2.05, nom, mono=True, gras=True, couleur=BLEU, taille=12)
        fleche(ax, (x + 0.7, 1.88), (x + 0.7, 1.45), couleur=BLEU)
        boite(ax, x, 0.75, 1.4, 0.7, val, fc="white", ec=GRIS, mono=True, taille=13)
        texte(ax, x + 0.7, 0.45, f"type : {typ}", taille=10, couleur=GRIS, italique=True)
    texte(ax, 0.02, 2.05, "nom", taille=9, couleur=GRIS, ha="left")
    sauver(fig, "fig_variables")


def fig_affectation():
    fig, ax = figure(7.6, 2.6)
    texte(ax, 3.8, 2.35, "x = x + 2", mono=True, taille=15, gras=True)
    # étape 1
    boite(ax, 0.2, 0.35, 3.3, 1.55, fc=GRIS_CL, ec=GRIS, lw=1)
    texte(ax, 1.85, 1.62, "① on calcule la partie droite", taille=10.5, gras=True)
    texte(ax, 1.85, 1.15, "x vaut 5, donc", taille=10.5)
    texte(ax, 1.85, 0.7, "x + 2  →  5 + 2  →  7", mono=True, taille=11.5, couleur=ORANGE)
    # étape 2
    boite(ax, 4.1, 0.35, 3.3, 1.55, fc=GRIS_CL, ec=GRIS, lw=1)
    texte(ax, 5.75, 1.62, "② on range le résultat dans x", taille=10.5, gras=True)
    texte(ax, 4.65, 0.85, "x", mono=True, taille=13, gras=True, couleur=BLEU)
    fleche(ax, (4.85, 0.85), (5.3, 0.85), couleur=BLEU)
    boite(ax, 5.35, 0.58, 0.75, 0.55, "5", fc="white", ec=GRIS, mono=True, ls="--")
    ax.plot([5.4, 6.05], [0.62, 1.09], color=ROUGE, lw=1.6)
    boite(ax, 6.3, 0.58, 0.75, 0.55, "7", fc=ORANGE_CL, ec=ORANGE, mono=True)
    fleche(ax, (3.55, 1.12), (4.05, 1.12), couleur=GRIS, lw=2)
    sauver(fig, "fig_affectation")


def fig_erreur():
    fig, ax = figure(8.2, 2.9)
    lignes = ["Traceback (most recent call last):",
              '  File "mon_script.py", line 2, in <module>',
              "    y = x + 2",
              "        ~~^~~",
              'TypeError: can only concatenate str (not "int") to str']
    boite(ax, 0.1, 0.95, 5.9, 1.85, fc="#FBFBFC", ec=GRIS, lw=1, rayon=0.03)
    for i, l in enumerate(lignes):
        c = ROUGE if i == 4 else "black"
        texte(ax, 0.22, 2.58 - i * 0.36, l, mono=True, taille=8.6, ha="left", couleur=c)
    # annotations
    boite(ax, 6.35, 2.15, 1.8, 0.55, "① où ? (ligne 2)", fc=BLEU_CL, ec=BLEU, taille=9.5)
    fleche(ax, (6.33, 2.38), (5.0, 2.22), couleur=BLEU, courbure=0.1)
    boite(ax, 6.35, 1.35, 1.8, 0.55, "② quelle ligne ?", fc=VERT_CL, ec=VERT, taille=9.5)
    fleche(ax, (6.33, 1.6), (2.0, 1.86), couleur=VERT, courbure=0.15)
    boite(ax, 0.6, 0.12, 2.6, 0.55, "③ quel type d'erreur ?", fc=ROUGE_CL, ec=ROUGE, taille=9.5)
    fleche(ax, (1.2, 0.68), (0.75, 1.0), couleur=ROUGE)
    boite(ax, 3.6, 0.12, 3.2, 0.55, "④ explication (à lire !)", fc=ORANGE_CL, ec=ORANGE, taille=9.5)
    fleche(ax, (4.4, 0.68), (3.6, 1.0), couleur=ORANGE)
    sauver(fig, "fig_erreur")


# --------------------------------------------------------------------------
# Chapitres 2 et 3 : conditions et boucles
# --------------------------------------------------------------------------
def fig_if():
    fig, ax = figure(7.6, 4.3)
    boite(ax, 2.6, 3.7, 2.0, 0.45, "t = 25", fc=GRIS_CL, ec=GRIS, mono=True)
    fleche(ax, (3.6, 3.7), (3.6, 3.38))
    losange(ax, 3.6, 2.98, 2.0, 0.8, "t <= 0 ?")
    fleche(ax, (4.6, 2.98), (5.5, 2.98), couleur=VERT)
    texte(ax, 5.05, 3.13, "oui", taille=9, couleur=VERT)
    boite(ax, 5.5, 2.73, 1.9, 0.5, '"solide"', fc=VERT_CL, ec=VERT, mono=True)
    fleche(ax, (3.6, 2.58), (3.6, 2.22), couleur=ROUGE)
    texte(ax, 3.82, 2.4, "non", taille=9, couleur=ROUGE)
    losange(ax, 3.6, 1.82, 2.0, 0.8, "t < 100 ?")
    fleche(ax, (4.6, 1.82), (5.5, 1.82), couleur=VERT)
    texte(ax, 5.05, 1.97, "oui", taille=9, couleur=VERT)
    boite(ax, 5.5, 1.57, 1.9, 0.5, '"liquide"', fc=VERT_CL, ec=VERT, mono=True,
          lw=3)
    fleche(ax, (3.6, 1.42), (3.6, 1.0), couleur=ROUGE)
    texte(ax, 3.82, 1.2, "non", taille=9, couleur=ROUGE)
    boite(ax, 2.65, 0.5, 1.9, 0.5, '"gazeux"', fc=VERT_CL, ec=VERT, mono=True)
    texte(ax, 0.1, 2.98, "if", mono=True, gras=True, couleur=ORANGE, ha="left", taille=12)
    texte(ax, 0.1, 1.82, "elif", mono=True, gras=True, couleur=ORANGE, ha="left", taille=12)
    texte(ax, 0.1, 0.75, "else", mono=True, gras=True, couleur=ORANGE, ha="left", taille=12)
    for y in (2.98, 1.82, 0.75):
        ax.plot([0.75, 2.45], [y, y], color=GRIS_CL, lw=1, ls=":")
    texte(ax, 6.45, 1.3, "← chemin suivi\n    pour t = 25", taille=9, couleur=GRIS,
          ha="left", va="top")
    texte(ax, 3.6, 0.2, "Un seul bloc est exécuté : le premier dont la condition est vraie.",
          taille=9.5, italique=True, couleur=GRIS)
    sauver(fig, "fig_if")


def fig_while():
    fig, ax = figure(6.6, 4.0)
    boite(ax, 1.6, 3.4, 2.4, 0.45, "x = 0", fc=GRIS_CL, ec=GRIS, mono=True)
    fleche(ax, (2.8, 3.4), (2.8, 3.07))
    losange(ax, 2.8, 2.65, 2.4, 0.84, "x <= 10 ?")
    fleche(ax, (2.8, 2.23), (2.8, 1.83), couleur=VERT)
    texte(ax, 3.02, 2.03, "oui", taille=9, couleur=VERT)
    boite(ax, 1.4, 0.98, 2.8, 0.85, "print(x)\nx = 2 * x + 2", fc=BLEU_CL, ec=BLEU,
          mono=True, taille=10.5)
    # retour
    ax.plot([1.4, 0.5, 0.5], [1.4, 1.4, 2.65], color=BLEU, lw=1.6)
    fleche(ax, (0.5, 2.65), (1.6, 2.65), couleur=BLEU)
    texte(ax, 0.35, 2.05, "on recommence", taille=9, couleur=BLEU, ha="center",
          italique=True)
    ax.texts[-1].set_rotation(90)
    fleche(ax, (4.0, 2.65), (4.9, 2.65), couleur=ROUGE)
    texte(ax, 4.45, 2.82, "non", taille=9, couleur=ROUGE)
    boite(ax, 4.9, 2.4, 1.55, 0.5, "suite du\nprogramme", fc=GRIS_CL, ec=GRIS, taille=9.5)
    texte(ax, 4.45, 1.35, "valeurs affichées :\n0, 2, 6\n(puis x vaut 14 → arrêt)",
          taille=9.5, ha="left", couleur=GRIS)
    texte(ax, 3.3, 0.45, "La condition est testée AVANT chaque tour.", taille=9.5,
          italique=True, couleur=GRIS)
    sauver(fig, "fig_while")


def fig_for():
    fig, ax = figure(6.8, 2.9)
    texte(ax, 0.1, 2.65, "for x in [1, 5, 7]:", mono=True, ha="left", taille=12, gras=True)
    texte(ax, 0.1, 2.3, "    print(x)", mono=True, ha="left", taille=12)
    vals = ["1", "5", "7"]
    for tour in range(3):
        y = 1.55 - tour * 0.62
        texte(ax, 0.1, y + 0.22, f"tour {tour + 1}", taille=10, ha="left", couleur=GRIS)
        cases(ax, 1.0, y, vals, l=0.6, h=0.44, surlignes=(tour,))
        fleche(ax, (3.0, y + 0.22), (3.5, y + 0.22))
        texte(ax, 3.65, y + 0.22, f"x vaut {vals[tour]}  →  affiche {vals[tour]}",
              mono=True, taille=10.5, ha="left")
    sauver(fig, "fig_for")


def fig_range():
    fig, ax = figure(7.0, 2.3)
    exemples = [("range(5)", list(range(5))), ("range(2, 6)", list(range(2, 6))),
                ("range(0, 10, 3)", list(range(0, 10, 3)))]
    for i, (code, vals) in enumerate(exemples):
        y = 1.75 - i * 0.7
        texte(ax, 0.1, y + 0.2, code, mono=True, ha="left", taille=11.5, gras=True)
        fleche(ax, (2.35, y + 0.2), (2.8, y + 0.2))
        cases(ax, 2.95, y, [str(v) for v in vals], l=0.52, h=0.4, taille=11)
    texte(ax, 5.7, 1.95, "la borne de fin\nest EXCLUE", taille=9.5, couleur=ROUGE,
          italique=True, ha="left")
    sauver(fig, "fig_range")


# --------------------------------------------------------------------------
# Chapitre 4 : fonctions
# --------------------------------------------------------------------------
def fig_fonction():
    fig, ax = figure(7.6, 2.6)
    texte(ax, 0.6, 1.75, "arguments", taille=10, couleur=GRIS, italique=True)
    boite(ax, 0.1, 0.95, 1.0, 0.55, "3", fc=ORANGE_CL, ec=ORANGE, mono=True, taille=13)
    texte(ax, 0.6, 0.7, "x = 3", mono=True, taille=9.5, couleur=ORANGE)
    fleche(ax, (1.15, 1.22), (1.85, 1.22), lw=2)
    boite(ax, 1.9, 0.3, 3.6, 1.95, fc=BLEU_CL, ec=BLEU, lw=2)
    texte(ax, 2.05, 2.0, "def carre_plus_un(x):", mono=True, ha="left", taille=10.5,
          gras=True, couleur=BLEU)
    texte(ax, 2.05, 1.55, "    y = x ** 2", mono=True, ha="left", taille=10.5)
    texte(ax, 2.05, 1.15, "    return y + 1", mono=True, ha="left", taille=10.5)
    texte(ax, 3.7, 0.6, "le corps de la fonction", taille=9.5, couleur=BLEU,
          italique=True)
    fleche(ax, (5.55, 1.22), (6.3, 1.22), lw=2)
    boite(ax, 6.35, 0.95, 1.0, 0.55, "10", fc=VERT_CL, ec=VERT, mono=True, taille=13)
    texte(ax, 6.85, 1.75, "valeur\nretournée", taille=10, couleur=GRIS, italique=True)
    texte(ax, 3.7, 0.0, "resultat = carre_plus_un(3)   →   resultat vaut 10",
          mono=True, taille=10)
    sauver(fig, "fig_fonction")


def fig_print_return():
    fig, ax = figure(7.6, 2.4)
    for i, (titre, code, bilan, c, ccl) in enumerate([
            ("avec print", "def f(x):\n    print(x * 2)", "affiche 6 à l'écran\nmais f(3) vaut None",
             ROUGE, ROUGE_CL),
            ("avec return", "def g(x):\n    return x * 2", "n'affiche rien\nmais g(3) vaut 6\n(réutilisable !)",
             VERT, VERT_CL)]):
        x0 = 0.1 + i * 3.8
        texte(ax, x0 + 1.75, 2.2, titre, gras=True, couleur=c)
        boite(ax, x0, 1.05, 3.5, 0.9, fc=GRIS_CL, ec=GRIS)
        texte(ax, x0 + 0.9, 1.5, code, mono=True, taille=10.5, ha="left")
        boite(ax, x0, 0.05, 3.5, 0.85, bilan, fc=ccl, ec=c, taille=10)
    sauver(fig, "fig_print_return")


# --------------------------------------------------------------------------
# Chapitre 5 : listes
# --------------------------------------------------------------------------
def fig_indices(nom="fig_indices", valeurs=('"a"', '"b"', '"c"', '"d"', '"e"'),
                titre="liste = [\"a\", \"b\", \"c\", \"d\", \"e\"]"):
    n = len(valeurs)
    fig, ax = figure(1.4 + n * 0.85, 2.5)
    texte(ax, 0.1, 2.25, titre, mono=True, ha="left", taille=11.5, gras=True)
    cx = cases(ax, 1.2, 0.95, valeurs, l=0.85, h=0.6, taille=12)
    texte(ax, 0.1, 1.83, "indice", taille=9.5, couleur=BLEU, ha="left")
    texte(ax, 0.1, 0.62, "indice\nnégatif", taille=9.5, couleur=ORANGE, ha="left")
    for i, c in enumerate(cx):
        texte(ax, c, 1.83, str(i), mono=True, couleur=BLEU, taille=12, gras=True)
        texte(ax, c, 0.62, str(i - n), mono=True, couleur=ORANGE, taille=12, gras=True)
    sauver(fig, nom)


def fig_slicing():
    vals = ['1', '5', '7', '8', '0', '9']
    fig, ax = figure(6.8, 2.6)
    texte(ax, 0.1, 2.35, "liste = [1, 5, 7, 8, 0, 9]", mono=True, ha="left", taille=11.5,
          gras=True)
    l = 0.85
    x0 = 1.2
    cases(ax, x0, 1.0, vals, l=l, h=0.6, surlignes=(2, 3, 4))
    for i in range(len(vals) + 1):
        x = x0 + i * l
        ax.plot([x, x], [0.85, 1.75], color=GRIS, lw=1, ls=":")
        texte(ax, x, 1.88, str(i), mono=True, couleur=BLEU, taille=11, gras=True)
    texte(ax, 0.1, 1.88, "« piquets »", taille=9, couleur=BLEU, ha="left")
    # accolade
    ax.annotate("", xy=(x0 + 2 * l, 0.75), xytext=(x0 + 5 * l, 0.75),
                arrowprops=dict(arrowstyle="|-|", color=ORANGE, lw=1.5))
    texte(ax, x0 + 3.5 * l, 0.42, "liste[2:5]  →  [7, 8, 0]", mono=True, couleur=ORANGE,
          taille=11)
    texte(ax, x0 + 3.5 * l, 0.08, "on coupe au piquet 2 et au piquet 5", taille=9.5,
          couleur=GRIS, italique=True)
    sauver(fig, "fig_slicing")


def fig_references():
    fig, ax = figure(8.7, 2.9)
    # gauche
    texte(ax, 1.9, 2.7, "liste2 = liste", mono=True, gras=True, couleur=ROUGE, taille=11.5)
    texte(ax, 0.3, 1.9, "liste", mono=True, gras=True, couleur=BLEU)
    texte(ax, 0.3, 0.95, "liste2", mono=True, gras=True, couleur=BLEU)
    cases(ax, 1.6, 1.15, ["1", "2", "7"], l=0.6, h=0.5)
    fleche(ax, (0.75, 1.9), (1.55, 1.5), couleur=BLEU)
    fleche(ax, (0.85, 0.95), (1.55, 1.25), couleur=BLEU)
    texte(ax, 1.9, 0.3, "1 seule liste, 2 noms :\nmodifier l'une modifie « l'autre »",
          taille=9.5, couleur=ROUGE, italique=True)
    ax.plot([4.0, 4.0], [0.1, 2.8], color=GRIS_CL, lw=1.5)
    # droite
    texte(ax, 6.0, 2.7, "liste2 = list(liste)", mono=True, gras=True, couleur=VERT,
          taille=11.5)
    texte(ax, 4.4, 1.9, "liste", mono=True, gras=True, couleur=BLEU)
    texte(ax, 4.4, 0.95, "liste2", mono=True, gras=True, couleur=BLEU)
    cases(ax, 5.7, 1.65, ["1", "2", "7"], l=0.6, h=0.5)
    cases(ax, 5.7, 0.7, ["1", "5", "7"], l=0.6, h=0.5)
    fleche(ax, (4.85, 1.9), (5.65, 1.9), couleur=BLEU)
    fleche(ax, (4.95, 0.95), (5.65, 0.95), couleur=BLEU)
    texte(ax, 6.0, 0.3, "2 listes indépendantes", taille=9.5, couleur=VERT, italique=True)
    texte(ax, 7.6, 1.9, "← après\nliste[1] = 2", taille=8.5, couleur=GRIS, ha="left")
    sauver(fig, "fig_references")


# --------------------------------------------------------------------------
# Chapitres 7 et 8 : dictionnaires, collections
# --------------------------------------------------------------------------
def fig_dictionnaire():
    fig, ax = figure(6.2, 2.9)
    texte(ax, 3.1, 2.7, 'stock = {"pomme": 3, "kiwi": 12, "poire": 0}', mono=True,
          taille=10.5, gras=True)
    texte(ax, 1.2, 2.25, "clés", gras=True, couleur=VIOLET)
    texte(ax, 4.5, 2.25, "valeurs", gras=True, couleur=VERT)
    for i, (k, v) in enumerate([('"pomme"', "3"), ('"kiwi"', "12"), ('"poire"', "0")]):
        y = 1.55 - i * 0.6
        boite(ax, 0.4, y, 1.6, 0.45, k, fc=VIOLET_CL, ec=VIOLET, mono=True)
        fleche(ax, (2.05, y + 0.22), (3.65, y + 0.22))
        boite(ax, 3.7, y, 1.6, 0.45, v, fc=VERT_CL, ec=VERT, mono=True)
    texte(ax, 3.1, 0.12, 'stock["kiwi"]  →  12', mono=True, couleur=ORANGE)
    sauver(fig, "fig_dictionnaire")


def fig_collections():
    fig, ax = figure(8.2, 2.5)
    items = [("liste", "[3, 1, 3]", "ordonnée,\nmodifiable,\ndoublons OK", BLEU, BLEU_CL),
             ("tuple", "(3, 1, 3)", "ordonné,\nNON modifiable,\ndoublons OK", GRIS, GRIS_CL),
             ("set", "{1, 3}", "sans ordre,\nmodifiable,\nsans doublon", VERT, VERT_CL),
             ("dict", '{"a": 3, "b": 1}', "clé → valeur,\nmodifiable,\nclés uniques",
              VIOLET, VIOLET_CL)]
    for i, (nom, ex, desc, c, ccl) in enumerate(items):
        x = 0.1 + i * 2.03
        boite(ax, x, 0.1, 1.9, 2.25, fc=ccl, ec=c)
        texte(ax, x + 0.95, 2.05, nom, gras=True, couleur=c, taille=12)
        texte(ax, x + 0.95, 1.6, ex, mono=True, taille=10)
        texte(ax, x + 0.95, 0.75, desc, taille=9.5)
    sauver(fig, "fig_collections")


# --------------------------------------------------------------------------
# Chapitres 9 et 10 : fichiers et numpy
# --------------------------------------------------------------------------
def fig_csv():
    fig, ax = figure(8.4, 3.0)
    texte(ax, 1.25, 2.8, "fichier entete.csv", gras=True, couleur=GRIS, taille=10)
    boite(ax, 0.1, 1.15, 2.3, 1.45, "NOM;PRENOM;AGE\nLemarchand;John;23\nTrias;Anne;",
          fc="#FBFBFC", ec=GRIS, mono=True, taille=9, rayon=0.02)
    # reader
    fleche(ax, (2.45, 2.2), (3.25, 2.45), lw=1.8)
    texte(ax, 2.85, 2.7, "csv.reader", mono=True, taille=9.5, couleur=BLEU)
    boite(ax, 3.3, 1.95, 5.0, 0.95,
          "['NOM', 'PRENOM', 'AGE']\n['Lemarchand', 'John', '23']\n['Trias', 'Anne', '']",
          fc=BLEU_CL, ec=BLEU, mono=True, taille=9)
    texte(ax, 8.25, 1.82, "une liste par ligne", taille=9, couleur=BLEU, ha="right",
          italique=True)
    # dictreader
    fleche(ax, (2.45, 1.5), (3.25, 1.0), lw=1.8)
    texte(ax, 2.6, 1.0, "csv.DictReader", mono=True, taille=9.5, couleur=VERT, ha="right")
    boite(ax, 3.3, 0.35, 5.0, 0.95,
          "{'NOM': 'Lemarchand', 'PRENOM': 'John', 'AGE': '23'}\n"
          "{'NOM': 'Trias', 'PRENOM': 'Anne', 'AGE': ''}",
          fc=VERT_CL, ec=VERT, mono=True, taille=8.5)
    texte(ax, 8.25, 0.18, "un dictionnaire par ligne (clés = en-tête)", taille=9,
          couleur=VERT, ha="right", italique=True)
    sauver(fig, "fig_csv")



def fig_lecture_ecriture():
    fig, ax = figure(7.8, 2.3)
    etapes_l = ['open(nom, "r")', "lire\n(readlines, csv, json)", "close()\n(ou with)"]
    etapes_e = ['open(nom, "w")', "écrire\n(write, writerow, dump)", "close() !\n(ou with)"]
    for j, (titre, etapes, c, ccl) in enumerate([("Lecture", etapes_l, BLEU, BLEU_CL),
                                                ("Écriture", etapes_e, ORANGE, ORANGE_CL)]):
        y = 1.35 - j * 1.15
        texte(ax, 0.05, y + 0.3, titre, gras=True, couleur=c, ha="left")
        for i, e in enumerate(etapes):
            x = 1.25 + i * 2.2
            boite(ax, x, y, 1.9, 0.62, e, fc=ccl, ec=c, taille=9.2,
                  mono=(i == 0))
            if i < 2:
                fleche(ax, (x + 1.92, y + 0.31), (x + 2.18, y + 0.31))
    sauver(fig, "fig_lecture_ecriture")



def fig_axis():
    fig, ax = figure(8.0, 3.2)
    notes = [["10", "12"], ["15", "16"], ["18", "12"]]
    x0, y0, l, h = 1.4, 0.55, 0.8, 0.55
    texte(ax, x0 + l, 2.95, "notes (3 examens × 2 étudiants)", taille=10, gras=True)
    for i, ligne in enumerate(notes):
        cases(ax, x0, y0 + (2 - i) * h, ligne, l=l, h=h)
        texte(ax, x0 - 0.15, y0 + (2 - i) * h + h / 2, f"examen {i}", taille=9,
              ha="right", couleur=GRIS)
    for j in range(2):
        texte(ax, x0 + j * l + l / 2, y0 + 3 * h + 0.15, f"étud. {j}", taille=9,
              couleur=GRIS)
    # axis=0
    fleche(ax, (x0 + 0.4, y0 + 3 * h - 0.05), (x0 + 0.4, y0 + 0.05), couleur=ORANGE, lw=2.5)
    fleche(ax, (x0 + 1.2, y0 + 3 * h - 0.05), (x0 + 1.2, y0 + 0.05), couleur=ORANGE, lw=2.5)
    texte(ax, x0 + l, 0.22, "notes.mean(axis=0) → [14.33, 13.33]", mono=True, taille=9.5,
          couleur=ORANGE)
    texte(ax, x0 + l, -0.08, "on « écrase » les lignes : un résultat par colonne",
          taille=8.5, couleur=ORANGE, italique=True)
    # axis=1
    x1 = 5.4
    for i, ligne in enumerate(notes):
        cases(ax, x1, y0 + (2 - i) * h, ligne, l=l, h=h)
        fleche(ax, (x1 + 0.05, y0 + (2 - i) * h + h / 2), (x1 + 2 * l - 0.05,
               y0 + (2 - i) * h + h / 2), couleur=VIOLET, lw=2.5)
    texte(ax, x1 + l, 0.22, "notes.mean(axis=1) → [11, 15.5, 15]", mono=True, taille=9.5,
          couleur=VIOLET)
    texte(ax, x1 + l, -0.08, "on « écrase » les colonnes : un résultat par ligne",
          taille=8.5, couleur=VIOLET, italique=True)
    sauver(fig, "fig_axis")



def fig_produits():
    fig, ax = figure(8.3, 2.5)
    A = [["0", "1"], ["2", "3"]]
    B = [["1", "0"], ["0", "1"]]

    def mat(x, y, M, coul=None):
        for i, ligne in enumerate(M):
            cases(ax, x, y + (1 - i) * 0.5, ligne, l=0.5, h=0.5, taille=11,
                  surlignes=coul or ())

    texte(ax, 1.95, 2.3, "A * B : élément par élément", gras=True, couleur=BLEU, taille=10.5)
    mat(0.1, 0.9, A); texte(ax, 1.3, 1.4, "*", taille=14)
    mat(1.5, 0.9, B); texte(ax, 2.7, 1.4, "=", taille=14)
    mat(2.9, 0.9, [["0", "0"], ["0", "3"]])
    texte(ax, 1.95, 0.45, "case (i, j) = A[i, j] × B[i, j]", taille=9, mono=True, couleur=GRIS)
    ax.plot([4.15, 4.15], [0.2, 2.4], color=GRIS_CL, lw=1.5)
    texte(ax, 6.1, 2.3, "A @ B : produit matriciel", gras=True, couleur=ORANGE, taille=10.5)
    mat(4.3, 0.9, A); texte(ax, 5.5, 1.4, "@", taille=14)
    mat(5.7, 0.9, B); texte(ax, 6.9, 1.4, "=", taille=14)
    mat(7.05, 0.9, A)
    texte(ax, 6.1, 0.45, "case (i, j) = ligne i de A · colonne j de B", taille=9, mono=True,
          couleur=GRIS)
    sauver(fig, "fig_produits")




# --------------------------------------------------------------------------
# Chapitres 11 à 13 : pandas et visualisation
# --------------------------------------------------------------------------
TABLE = [["Adelie", "Torgersen", "39.1", "3750"],
         ["Adelie", "Dream", "37.8", "3400"],
         ["Gentoo", "Biscoe", "46.1", "4500"],
         ["Chinstrap", "Dream", "46.5", "3500"],
         ["Gentoo", "Biscoe", "50.0", "5700"]]
COLONNES = ["species", "island", "bill_length_mm", "body_mass_g"]


def tableau(ax, x0, y0, lignes, colonnes, index, largeurs, h=0.42, taille=9.5,
            fc_cellule=lambda i, j: "white", ec=GRIS, fc_entete=GRIS_CL, fc_index=GRIS_CL):
    """Dessine un tableau ; (x0, y0) = coin supérieur gauche. Renvoie les abscisses."""
    xs = [x0]
    for l in largeurs:
        xs.append(xs[-1] + l)
    # en-tête
    boite(ax, xs[0], y0 - h, largeurs[0], h, "", fc=fc_entete, ec=ec, rayon=0, lw=1)
    for j, c in enumerate(colonnes):
        boite(ax, xs[j + 1], y0 - h, largeurs[j + 1], h, c, fc=fc_entete, ec=ec, rayon=0,
              lw=1, mono=True, taille=taille, gras=True)
    for i, ligne in enumerate(lignes):
        y = y0 - (i + 2) * h
        boite(ax, xs[0], y, largeurs[0], h, str(index[i]), fc=fc_index, ec=ec, rayon=0, lw=1,
              mono=True, taille=taille, couleur_texte=GRIS)
        for j, v in enumerate(ligne):
            boite(ax, xs[j + 1], y, largeurs[j + 1], h, v, fc=fc_cellule(i, j), ec=ec, rayon=0,
                  lw=1, mono=True, taille=taille)
    return xs


def fig_dataframe():
    fig, ax = figure(8.6, 3.9)
    larg = [0.45, 1.25, 1.35, 1.85, 1.65]

    def couleur(i, j):
        if j == 3:
            return VERT_CL
        if i == 2:
            return ORANGE_CL
        return "white"
    xs = tableau(ax, 1.0, 3.2, TABLE, COLONNES, range(5), larg, fc_cellule=couleur)
    h = 0.42
    # annotations
    texte(ax, 0.15, 3.2 - 4 * h, "index", couleur=GRIS, taille=10, gras=True, ha="left")
    fleche(ax, (0.62, 3.2 - 4 * h), (1.0, 3.2 - 4 * h), couleur=GRIS)
    texte(ax, (xs[1] + xs[3]) / 2, 3.65, "noms des colonnes (df.columns)", couleur=GRIS,
          taille=10, gras=True)
    fleche(ax, ((xs[1] + xs[3]) / 2, 3.52), ((xs[1] + xs[3]) / 2, 3.24), couleur=GRIS)
    texte(ax, (xs[4] + xs[5]) / 2, 0.42, 'une colonne = une Series\ndf["body_mass_g"]',
          couleur=VERT, taille=10, gras=True)
    xr = xs[5] + 0.1
    yr = 3.2 - 3.5 * h
    fleche(ax, (xr + 0.35, yr), (xr + 0.02, yr), couleur=ORANGE)
    texte(ax, xr + 0.4, yr, "une ligne =\nune observation\n(un manchot)", couleur=ORANGE,
          taille=10, gras=True, ha="left")
    texte(ax, 4.3, 0.0, "df.shape  →  (344, 7) : 344 lignes et 7 colonnes au total",
          mono=True, taille=9.5, couleur=GRIS)
    sauver(fig, "fig_dataframe")


def fig_loc_iloc():
    fig, ax = figure(8.2, 2.9)
    lignes = [["14", "17", "12"], ["9", "12", "15"], ["16", "13", "18"]]
    index = ["Aude", "Yanis", "Maëlle"]

    def couleur(i, j):
        return ORANGE_CL if (i == 1 and j == 1) else "white"
    xs = tableau(ax, 0.2, 2.3, lignes, ["maths", "info", "anglais"], index,
                 [0.95, 0.9, 0.9, 1.0], fc_cellule=couleur, taille=10)
    texte(ax, 2.15, 2.6, "notes (index = prénoms)", gras=True, taille=10)
    texte(ax, 4.6, 1.95, 'notes.loc["Yanis", "info"]', mono=True, taille=10.5,
          couleur=BLEU, ha="left", gras=True)
    texte(ax, 4.6, 1.62, "loc : par NOMS (étiquettes)", taille=9.5, couleur=BLEU,
          ha="left", italique=True)
    texte(ax, 4.6, 1.05, "notes.iloc[1, 1]", mono=True, taille=10.5, couleur=VIOLET,
          ha="left", gras=True)
    texte(ax, 4.6, 0.72, "iloc : par POSITIONS (entiers, à partir de 0)", taille=9.5,
          couleur=VIOLET, ha="left", italique=True)
    texte(ax, 4.6, 0.25, "→ les deux désignent la même case : 12", taille=9.5,
          couleur=ORANGE, ha="left")
    sauver(fig, "fig_loc_iloc")


def fig_filtre():
    fig, ax = figure(9.0, 3.3)
    larg = [0.4, 1.15, 1.2]
    lignes = [[r[0], r[3]] for r in TABLE]
    tableau(ax, 0.1, 2.95, lignes, ["species", "body_mass_g"], range(5), larg, taille=9)
    h = 0.42
    texte(ax, 1.5, 3.2, "df", mono=True, gras=True)
    masque = [int(r[3]) > 4000 for r in TABLE]
    x_m = 3.35
    texte(ax, x_m + 0.55, 3.2, 'df["body_mass_g"] > 4000', mono=True, taille=8.8, gras=True,
          couleur=BLEU)
    for i, m in enumerate(masque):
        y = 2.95 - (i + 2) * h
        boite(ax, x_m, y, 1.1, h, str(m), fc=VERT_CL if m else ROUGE_CL,
              ec=VERT if m else ROUGE, rayon=0, lw=1, mono=True, taille=9)
    fleche(ax, (4.6, 1.65), (5.25, 1.65), lw=2)
    gardees = [(i, l) for i, l in enumerate(lignes) if masque[TABLE.index(TABLE[i])]]
    tableau(ax, 5.35, 2.95, [l for _, l in gardees], ["species", "body_mass_g"],
            [i for i, _ in gardees], larg, taille=9, fc_cellule=lambda i, j: VERT_CL)
    texte(ax, 6.75, 3.2, 'df[df["body_mass_g"] > 4000]', mono=True, taille=8.8, gras=True,
          couleur=VERT)
    texte(ax, 4.5, 0.12, "On ne garde que les lignes pour lesquelles le masque vaut True"
          " (l'index d'origine est conservé).", taille=9, italique=True, couleur=GRIS)
    sauver(fig, "fig_filtre")


def fig_groupby():
    fig, ax = figure(9.4, 3.6)
    donnees = [("Adelie", "3750"), ("Gentoo", "4500"), ("Adelie", "3400"),
               ("Gentoo", "5700"), ("Chinstrap", "3500"), ("Adelie", "3800")]
    couleurs = {"Adelie": (BLEU, BLEU_CL), "Gentoo": (VERT, VERT_CL),
                "Chinstrap": (VIOLET, VIOLET_CL)}
    texte(ax, 1.25, 3.4, "① le tableau", gras=True, taille=10)
    for i, (e, m) in enumerate(donnees):
        c, ccl = couleurs[e]
        y = 2.9 - i * 0.42
        boite(ax, 0.1, y, 1.3, 0.42, e, fc=ccl, ec=c, rayon=0, lw=1, mono=True, taille=9)
        boite(ax, 1.4, y, 0.8, 0.42, m, fc=ccl, ec=c, rayon=0, lw=1, mono=True, taille=9)
    # split
    texte(ax, 3.9, 3.4, "② séparer (split)", gras=True, taille=10)
    groupes = {"Adelie": ["3750", "3400", "3800"], "Gentoo": ["4500", "5700"],
               "Chinstrap": ["3500"]}
    y = 2.95
    centres = {}
    for e, ms in groupes.items():
        c, ccl = couleurs[e]
        texte(ax, 3.0, y - 0.05, e, mono=True, taille=9, couleur=c, ha="right", gras=True)
        for k, m in enumerate(ms):
            boite(ax, 3.1 + k * 0.62, y - 0.25, 0.62, 0.4, m, fc=ccl, ec=c, rayon=0, lw=1,
                  mono=True, taille=9)
        centres[e] = y - 0.05
        y -= 0.85
    fleche(ax, (2.3, 1.9), (2.55, 1.9), lw=2)
    # apply
    texte(ax, 6.2, 3.4, "③ calculer (apply)", gras=True, taille=10)
    moyennes = {"Adelie": "3650", "Gentoo": "5100", "Chinstrap": "3500"}
    for e, yc in centres.items():
        c, ccl = couleurs[e]
        fleche(ax, (5.1, yc), (5.55, yc), couleur=c)
        texte(ax, 5.62, yc, f"moyenne → {moyennes[e]}", taille=9, couleur=c, ha="left",
              mono=True)
    # combine
    texte(ax, 8.4, 3.4, "④ combiner", gras=True, taille=10)
    for i, e in enumerate(groupes):
        c, ccl = couleurs[e]
        y = 2.7 - i * 0.42
        boite(ax, 7.75, y, 1.0, 0.42, e, fc=ccl, ec=c, rayon=0, lw=1, mono=True, taille=8.5)
        boite(ax, 8.75, y, 0.6, 0.42, moyennes[e], fc=ccl, ec=c, rayon=0, lw=1, mono=True,
              taille=8.5)
    texte(ax, 4.7, 0.05, 'df.groupby("species")["body_mass_g"].mean()', mono=True,
          taille=10.5, gras=True, couleur=ORANGE)
    sauver(fig, "fig_groupby")


def fig_choix_graphique():
    import numpy as np
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(2, 3, figsize=(9.6, 5.6))
    fig.subplots_adjust(hspace=0.75, wspace=0.35)
    titres = [("Distribution d'une variable\nnumérique", "histogramme : hist, histplot"),
              ("Comparer une variable\nentre des groupes", "boîtes : boxplot"),
              ("Comparer des effectifs ou\ndes moyennes par catégorie", "barres : bar, barplot, countplot"),
              ("Relation entre deux\nvariables numériques", "nuage de points : scatter"),
              ("Évolution dans le temps", "courbe : plot, lineplot"),
              ("Corrélations entre\nplusieurs variables", "carte de chaleur : heatmap")]
    a = axes.ravel()
    a[0].hist(rng.normal(0, 1, 400), bins=20, color=BLEU, edgecolor="white")
    a[1].boxplot([rng.normal(m, 1, 80) for m in (0, 1.2, 0.5)], patch_artist=True,
                 boxprops=dict(facecolor=BLEU_CL, color=BLEU), medianprops=dict(color=ORANGE))
    a[2].bar(["A", "B", "C"], [12, 7, 9], color=[BLEU, VERT, VIOLET])
    x = rng.uniform(0, 10, 60)
    a[3].scatter(x, 2 * x + rng.normal(0, 3, 60), color=BLEU, s=14)
    t = np.arange(48)
    a[4].plot(t, 100 + 2 * t + 15 * np.sin(t / 2), color=BLEU)
    corr = np.array([[1, .8, -.3], [.8, 1, -.1], [-.3, -.1, 1]])
    a[5].imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    for i in range(3):
        for j in range(3):
            a[5].text(j, i, f"{corr[i, j]:.1f}", ha="center", va="center", fontsize=8,
                       color="white" if abs(corr[i, j]) > 0.5 else "black")
    for ax, (q, r) in zip(a, titres):
        ax.set_title(q, fontsize=10, weight="bold")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel(r, fontsize=9, color=ORANGE, family=MONO if False else None)
        for sp in ax.spines.values():
            sp.set_color(GRIS)
    sauver(fig, "fig_choix_graphique")


def fig_anatomie_graphique():
    import numpy as np
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    annees = np.arange(1949, 1961)
    # totaux annuels du jeu de données flights (content/donnees/flights.csv)
    valeurs = [1520, 1676, 2042, 2364, 2700, 2867, 3408, 3939, 4421, 4572, 5140, 5714]
    ax.plot(annees, valeurs, marker="o", color=BLEU, label="passagers")
    ax.set_title("Nombre de passagers par an", weight="bold")
    ax.set_xlabel("Année")
    ax.set_ylabel("Passagers (milliers)")
    ax.set_ylim(1200, 6600)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    style = dict(fontsize=9.5, color=ORANGE, family=MONO, weight="bold",
                 arrowprops=dict(arrowstyle="-|>", color=ORANGE), xycoords="axes fraction",
                 textcoords="axes fraction", annotation_clip=False)
    ax.annotate("ax.set_title(...)", xy=(0.66, 1.04), xytext=(0.72, 0.9), **style)
    ax.annotate("ax.set_xlabel(...)", xy=(0.56, -0.13), xytext=(0.66, 0.08), **style)
    ax.annotate("ax.set_ylabel(...)", xy=(-0.06, 0.62), xytext=(0.06, 0.62), **style)
    ax.annotate("ax.legend()", xy=(0.2, 0.93), xytext=(0.3, 0.8), **style)
    ax.annotate('ax.plot(x, y, marker="o")', xy=(0.75, 0.62), xytext=(0.6, 0.3), **style)
    sauver(fig, "fig_anatomie_graphique")


FIGURES = [fig_variables, fig_affectation, fig_erreur, fig_if, fig_while, fig_for,
           fig_range, fig_fonction, fig_print_return, fig_indices, fig_slicing,
           fig_references, fig_dictionnaire, fig_collections, fig_csv,
           fig_lecture_ecriture, fig_axis, fig_produits, fig_dataframe, fig_loc_iloc,
           fig_filtre, fig_groupby, fig_choix_graphique, fig_anatomie_graphique]

if __name__ == "__main__":
    for f in FIGURES:
        f()
    fig_indices("fig_indices_chaine", ('"P"', '"y"', '"t"', '"h"', '"o"', '"n"'),
                's = "Python"')
    print("Figures générées dans", DOSSIER)
