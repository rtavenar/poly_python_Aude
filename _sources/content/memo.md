---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.5.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(ch:memo)=
# Fiche mémo

Cette fiche rassemble la syntaxe essentielle vue dans ce document. Elle ne remplace pas les chapitres, mais vous permet de retrouver rapidement une notation.

## Bases (chapitres 1 à 4)

```python
# Variables, types, conversions
x = 12                 # int
y = 3.5                # float
nom = "Aude"           # str
ok = True              # bool (True / False), et la valeur spéciale None
type(x)                # <class 'int'>
int("12"), float("3.5"), str(12)

# Opérateurs
7 + 2, 7 - 2, 7 * 2, 7 / 2    # 9, 5, 14, 3.5
7 // 2, 7 % 2, 7 ** 2         # 3 (quotient), 1 (reste), 49 (puissance)
x += 1                        # x = x + 1

# Affichage
print("x vaut", x)
print(f"{nom} a {x} ans, prix : {y:.2f} euros")

# Comparaisons et logique
x == 12, x != 12, x < 12, x >= 12, x in [1, 12]
(x > 0) and (x < 20), (x < 0) or (x > 20), not ok

# Conditions
if x > 0:
    print("positif")
elif x < 0:
    print("négatif")
else:
    print("nul")

# Boucles
while x > 0:
    x = x - 3
for i in range(5):            # 0, 1, 2, 3, 4
    print(i)
for i in range(2, 10, 2):     # 2, 4, 6, 8
    print(i)

# Fonctions
def aire(largeur, longueur=1):
    """Retourne l'aire d'un rectangle."""
    return largeur * longueur

a = aire(3, 4)
a = aire(longueur=4, largeur=3)

# Modules
import math
import random
import numpy as np
math.sqrt(2), math.pi, random.randint(1, 6)
```

## Listes (chapitre 5)

```python
l = [1, 5, 7]
len(l), l[0], l[-1], l[1:3], l[:2], l[2:]
l[0] = 2                         # modification
l.append(4)                      # ajout à la fin
l.insert(0, 9)                   # insertion à l'indice 0
del l[0]                         # suppression par indice
l.remove(7)                      # suppression de la première occurrence de 7
5 in l, l.index(5)               # recherche
l + [8, 9], 3 * [0]              # concaténation, répétition
sorted(l), sorted(l, reverse=True)
sum(l), min(l), max(l)
copie = list(l)                  # vraie copie (et non copie = l)

for elem in l: ...               # parcours des éléments
for i in range(len(l)): ...      # parcours des indices
for i, elem in enumerate(l): ... # indices et éléments
for a, b in zip(l1, l2): ...     # deux listes en parallèle

carres = [i ** 2 for i in range(10) if i % 2 == 0]   # liste en compréhension
```

## Chaînes de caractères (chapitre 6)

```python
s = "Bonjour"
len(s), s[0], s[-1], s[1:4], "jour" in s
s.lower(), s.upper(), s.strip(), s.replace("o", "0")
"a;b;c".split(";")          # ['a', 'b', 'c']
"-".join(["a", "b", "c"])   # 'a-b-c'
s.count("o"), s.find("j"), s.startswith("Bon"), s.endswith("!")
f"{3.14159:.2f}", f"{42:5d}", f"{'ab':<6}|", f"{'ab':>6}|"
```

## Dictionnaires, _tuples_, _sets_ (chapitre 7)

```python
d = {"pomme": 3, "kiwi": 12}
d["pomme"], d.get("banane", 0), "kiwi" in d
d["banane"] = 6                  # ajout ou modification
del d["kiwi"]
for cle in d.keys(): ...
for valeur in d.values(): ...
for cle, valeur in d.items(): ...
d[mot] = d.get(mot, 0) + 1       # compter des occurrences

t = (3, 7)                       # tuple (non modifiable)
x, y = t                         # déballage
a, b = b, a                      # échange

e = {1, 2, 3}                    # set (sans ordre ni doublon) ; set() pour un set vide
e.add(4), e.remove(1)
set(liste)                       # supprimer les doublons
e1 | e2, e1 & e2, e1 - e2        # union, intersection, différence
```

## Tests (chapitre 8)

```python
def test_ma_fonction():
    assert ma_fonction(2) == 4
    assert ma_fonction(0) == 0          # cas limite
    assert abs(ma_fonction(0.1) - 0.2) < 1e-9   # résultat à virgule
    print("OK")
```

## Fichiers (chapitre 9)

```python
import os, csv, json

os.listdir("donnees"), os.path.join("donnees", "notes.csv")

with open("texte.txt", "r", encoding="utf-8") as fp:      # "r" lire, "w" écrire, "a" ajouter
    for ligne in fp.readlines():
        ligne = ligne.strip()

with open("notes.csv", "r", encoding="utf-8") as fp:
    for ligne in csv.DictReader(fp, delimiter=";"):     # ou csv.reader : une liste par ligne
        note = float(ligne["maths"])

with open("sortie.txt", "w", encoding="utf-8", newline="\n") as fp:
    fp.write("texte\n")
    csv.writer(fp, delimiter=";").writerow([1, 2, 3])

with open("donnees.json", "r", encoding="utf-8") as fp:
    donnees = json.load(fp)                 # json.loads(chaine) pour une chaîne
with open("sortie.json", "w", encoding="utf-8") as fp:
    json.dump(donnees, fp, indent=2)
```

## `numpy` (chapitre 10)

```python
import numpy as np
A = np.array([[0, 1], [2, 3]])
A.shape, A.ndim, A.dtype, A.T
A[1, 0], A[:, 0], A[0, :], A[0:2, 1:]
A * A, A ** 2, A @ A                        # élément par élément vs produit matriciel
np.zeros((2, 3)), np.ones((2, 3)), np.eye(2), np.arange(10), np.linspace(0, 1, 11)
np.arange(10).reshape((5, 2))
A.sum(), A.mean(), A.std(), A.min(), A.max()
A.mean(axis=0)                              # un résultat par colonne
A.mean(axis=1)                              # un résultat par ligne
A > 1, np.sum(A > 1), A[A > 1]              # masques
```

## `pandas` (chapitres 11 et 12)

```python
import pandas as pd
df = pd.read_csv("donnees.csv", sep=";", decimal=",")   # encoding="iso-8859-1" si besoin

# Explorer
df.head(), df.shape, df.columns, df.dtypes
df.info(), df.describe()
df["col"].value_counts(), df["col"].unique(), df["col"].nunique()
df["col"].mean(), df["col"].median(), df["col"].std(), df["col"].min()

# Sélectionner
df["col"]                                   # une colonne (Series)
df[["col1", "col2"]]                        # plusieurs colonnes (DataFrame)
df[df["age"] > 18]                          # filtrer des lignes
df[(df["age"] > 18) & (df["sexe"] == "F")]  # & (et), | (ou), ~ (non), parenthèses !
df[df["ville"].isin(["Rennes", "Brest"])]
df.loc[df["age"] > 18, ["nom", "age"]]      # par noms (fin incluse)
df.iloc[0:5, 0:2]                           # par positions (fin exclue)
df.sort_values("col", ascending=False)

# Transformer
df["c"] = df["a"] / df["b"]
df["cat"] = df["code"].map({"F": "femme", "H": "homme"})
df["classe"] = pd.cut(df["age"], bins=[0, 18, 60, 120], labels=["jeune", "adulte", "senior"])
df["d"] = df["col"].apply(ma_fonction)
df = df.rename(columns={"ancien": "nouveau"})
df = df.drop(columns=["inutile"])
df["col"].str.lower(), df["col"].str.contains("motif")
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y");  df["date"].dt.year

# Valeurs manquantes
df.isna().sum()
df = df.dropna(subset=["col"])
df["col"] = df["col"].fillna(df["col"].median())

# Résumer par groupe
df.groupby("cat")["num"].mean()
df.groupby(["cat1", "cat2"])["num"].agg(["count", "mean"])
df.groupby("cat").agg(effectif=("num", "count"), moyenne=("num", "mean"))
pd.crosstab(df["cat1"], df["cat2"], normalize="index")

# Combiner et enregistrer
pd.merge(df1, df2, on="cle", how="left")
pd.concat([df1, df2])
df.to_csv("resultat.csv", index=False)
```

## Visualisation (chapitre 13)

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x, y, marker="o", label="série")    # courbe
ax.scatter(x, y)                            # nuage de points
ax.hist(valeurs, bins=20)                   # histogramme
ax.bar(categories, hauteurs)                # barres
ax.set_title("Titre"); ax.set_xlabel("x (unité)"); ax.set_ylabel("y (unité)"); ax.legend()
fig.savefig("graphique.png", dpi=150)       # AVANT plt.show()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))   # plusieurs graphiques : axes[0], axes[1]

df["col"].plot(kind="hist")                 # raccourci pandas

sns.histplot(data=df, x="num", hue="cat")
sns.boxplot(data=df, x="cat", y="num")
sns.barplot(data=df, x="cat", y="num")      # moyenne par catégorie
sns.countplot(data=df, x="cat")
sns.scatterplot(data=df, x="num1", y="num2", hue="cat")
sns.lineplot(data=df, x="date", y="num")
sns.heatmap(df.select_dtypes("number").corr(), annot=True, cmap="RdBu_r", vmin=-1, vmax=1)
sns.pairplot(data=df, hue="cat")
```

## Modélisation (chapitre 14)

```python
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats

m = smf.ols("y ~ x1 + C(cat) + x1:x2", data=df).fit()      # lm(y ~ x1 + factor(cat) + x1:x2)
m.summary(), m.params, m.pvalues, m.conf_int(), m.rsquared, m.resid
m.predict(nouveau_df)
sm.stats.anova_lm(m, typ=2)                               # table d'ANOVA
sm.stats.anova_lm(m_simple, m_complet)                    # comparaison de modèles emboîtés

lg = smf.logit("y01 ~ x + C(cat)", data=df).fit()          # glm(..., family = binomial)
np.exp(lg.params)                                         # odds ratios

stats.ttest_ind(a, b, equal_var=False)                    # t.test (Welch)
stats.chi2_contingency(pd.crosstab(df["a"], df["b"]))     # chisq.test
stats.pearsonr(x, y)                                      # cor.test
```

## Correspondances R / SAS / Python

| R | SAS | Python |
|---|---|---|
| `x <- 5` | `x = 5;` | `x = 5` |
| `x[1]` (premier élément) | | `x[0]` |
| `x[-1]` (tout sauf le premier) | | `x[1:]` (et `x[-1]` = le dernier !) |
| `1:10` | `DO i = 1 TO 10;` | `range(1, 11)` |
| `function(x) { ... }` | `%macro` | `def f(x): ... return ...` |
| `library(pkg)` | | `import pkg` |
| `read.csv` | `PROC IMPORT` | `pd.read_csv` |
| `summary(df)` | `PROC MEANS` | `df.describe()` |
| `table(x)` | `PROC FREQ` | `df["x"].value_counts()` |
| `filter`, `select`, `arrange` | `WHERE`, `KEEP`, `PROC SORT` | `df[masque]`, `df[["x", "y"]]`, `df.sort_values("x")` |
| `mutate` | étape DATA | `df["z"] = ...` |
| `group_by` + `summarise` | `PROC MEANS; CLASS` | `df.groupby("g")["x"].mean()` |
| `left_join` / `merge` | `MERGE; BY` | `pd.merge(a, b, on="id", how="left")` |
| `ggplot2` | `PROC SGPLOT` | `seaborn` (ou `plotnine`) |
| `lm`, `glm` | `PROC REG`, `PROC LOGISTIC` | `smf.ols`, `smf.logit`, `smf.glm` |
| `NA`, `is.na` | `.`, `MISSING` | `NaN`, `isna()` |

## Les erreurs les plus courantes

| Erreur | Cause probable |
|---|---|
| `SyntaxError` | `:` ou parenthèse ou guillemet oublié ; `=` au lieu de `==` |
| `IndentationError` | décalage manquant ou incohérent |
| `NameError` | faute de frappe, variable non définie, module non importé |
| `TypeError` | opération entre types incompatibles (`"12" + 2`), mauvais nombre d'arguments |
| `ValueError` | conversion impossible (`int("douze")`) |
| `IndexError` | indice trop grand (`l[len(l)]`) |
| `KeyError` | clé absente d'un dictionnaire, ou nom de colonne inexistant dans un `DataFrame` |
| `AttributeError` | méthode ou attribut inexistant (`None.append`…) |
| `ZeroDivisionError` | division par zéro |
| `FileNotFoundError` | mauvais nom de fichier ou mauvais dossier |
| `ValueError: The truth value of a Series is ambiguous` | `and` / `or` utilisés au lieu de `&` / `\|` pour combiner des filtres `pandas` |
