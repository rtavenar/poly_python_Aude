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

(ch:projets)=
# Mini-projets

Vous avez maintenant tous les outils pour mener une petite analyse de données de bout en bout.
Les mini-projets de ce chapitre vous proposent de les mettre en pratique sur des problèmes plus longs, qui mobilisent plusieurs chapitres à la fois.

```{admonition} Comment aborder un projet ?
:class: tip

* **Lisez tout l'énoncé** avant de commencer.
* **Avancez étape par étape**, en vérifiant chaque résultat intermédiaire (affichez `head()`, `shape`, les valeurs obtenues…) avant de passer à la suite.
* Travaillez dans un **notebook** : alternez cellules de code et cellules de texte (_Markdown_) dans lesquelles vous écrivez vos observations et vos conclusions. Un bon notebook d'analyse se lit comme un petit rapport.
* Ne regardez la solution qu'à la toute fin… et sachez qu'il existe beaucoup de solutions correctes !
```

| Projet | Chapitres mobilisés | Difficulté |
|---|---|---|
| 1. Bulletins de notes en Python « pur » | 4, 5, 7, 9 | ★★ |
| 2. Les manchots de l'archipel Palmer | 11 à 14 | ★★ |
| 3. Qui a survécu au naufrage du Titanic ? | 11 à 14 | ★★★ |

## Projet 1 : Bulletins de notes en Python « pur » ★★

_Chapitres mobilisés : 4, 5, 7 et 9._

Ce premier projet n'utilise pas `pandas` : il vous fait pratiquer les bases (fonctions, listes, dictionnaires, fichiers) sur lesquelles tout le reste repose. Vous pourrez ensuite comparer avec la version `pandas` (étape 8).

Le fichier `donnees/notes.csv` contient les notes de 8 étudiants dans trois matières.
On souhaite produire des statistiques par matière et un bulletin pour chaque étudiant.

```
nom;prenom;maths;info;anglais
Martin;Aude;14;17;12
Benali;Yanis;9;12;15
Le Goff;Maëlle;16;13;18
Dupont;Hugo;7;10;9
Nguyen;Linh;12;19;14
Kerbrat;Erwan;11;8;13
Diallo;Fatou;15;14;16
Moreau;Inès;10;11;8
```

### Étapes

1. Écrivez une fonction `charge_notes(nom_fichier)` qui lit le fichier et retourne une **liste de dictionnaires**, un par étudiant, dans lesquels les notes ont été converties en nombres. Par exemple, le premier élément doit être `{"nom": "Martin", "prenom": "Aude", "maths": 14.0, "info": 17.0, "anglais": 12.0}`.
2. Écrivez une fonction `moyenne_etudiant(etudiant, matieres)` qui retourne la moyenne d'un étudiant (un dictionnaire) sur une liste de matières.
3. Écrivez une fonction `stats_matiere(etudiants, matiere)` qui retourne un _tuple_ `(minimum, moyenne, maximum)` des notes d'une matière.
4. Écrivez une fonction `mention(moyenne)` qui retourne la mention correspondant à une moyenne (voir l'exercice 2.3).
5. Écrivez une fonction `rang(etudiants, matieres)` qui retourne la liste des noms complets des étudiants (prénom et nom), classés par moyenne décroissante.
6. Écrivez une fonction `ecrit_bulletins(etudiants, matieres, nom_fichier)` qui produit un fichier texte contenant un bulletin pour chaque étudiant, de la forme :

```text
=== Bulletin de Aude Martin ===
maths   : 14.0
info    : 17.0
anglais : 12.0
Moyenne : 14.33 (Bien)
Rang    : 4 / 8
```

7. **Bonus** : les matières n'ont pas toutes la même importance. Ajoutez des coefficients (stockés dans un dictionnaire `{"maths": 3, "info": 3, "anglais": 1}`) au calcul de la moyenne.
8. **Pour comparer** : refaites les étapes 1 à 3 avec `pandas` (chapitres 11 et 12). Combien de lignes de code faut-il ?

```{raw} latex
\iffalse
```

```{admonition} Indice pour l'étape 5
:class: hint, dropdown

Construisez une liste de _tuples_ `(moyenne, nom_complet)`, puis triez-la avec `sorted(..., reverse=True)`.
```

````{admonition} Solution complète
:class: tip, dropdown

```python
import csv

MATIERES = ["maths", "info", "anglais"]

def charge_notes(nom_fichier):
    etudiants = []
    with open(nom_fichier, "r", encoding="utf-8") as fp:
        for ligne in csv.DictReader(fp, delimiter=";"):
            for matiere in MATIERES:
                ligne[matiere] = float(ligne[matiere])
            etudiants.append(ligne)
    return etudiants

def moyenne_etudiant(etudiant, matieres):
    total = 0
    for matiere in matieres:
        total += etudiant[matiere]
    return total / len(matieres)

def stats_matiere(etudiants, matiere):
    notes = []
    for etudiant in etudiants:
        notes.append(etudiant[matiere])
    return min(notes), sum(notes) / len(notes), max(notes)

def mention(moyenne):
    if moyenne >= 16:
        return "Très bien"
    elif moyenne >= 14:
        return "Bien"
    elif moyenne >= 12:
        return "Assez bien"
    elif moyenne >= 10:
        return "Passable"
    else:
        return "Ajourné"

def nom_complet(etudiant):
    return f"{etudiant['prenom']} {etudiant['nom']}"

def rang(etudiants, matieres):
    couples = []
    for etudiant in etudiants:
        couples.append((moyenne_etudiant(etudiant, matieres), nom_complet(etudiant)))
    classement = []
    for moyenne, nom in sorted(couples, reverse=True):
        classement.append(nom)
    return classement

def ecrit_bulletins(etudiants, matieres, nom_fichier):
    classement = rang(etudiants, matieres)
    with open(nom_fichier, "w", encoding="utf-8", newline="\n") as fp:
        for etudiant in etudiants:
            nom = nom_complet(etudiant)
            moyenne = moyenne_etudiant(etudiant, matieres)
            fp.write(f"=== Bulletin de {nom} ===\n")
            for matiere in matieres:
                fp.write(f"{matiere:<8}: {etudiant[matiere]}\n")
            fp.write(f"Moyenne : {moyenne:.2f} ({mention(moyenne)})\n")
            fp.write(f"Rang    : {classement.index(nom) + 1} / {len(etudiants)}\n\n")

etudiants = charge_notes("donnees/notes.csv")
assert etudiants[0] == {"nom": "Martin", "prenom": "Aude", "maths": 14.0, "info": 17.0, "anglais": 12.0}
for matiere in MATIERES:
    mini, moy, maxi = stats_matiere(etudiants, matiere)
    print(f"{matiere:<8} min = {mini:5.1f}  moyenne = {moy:5.2f}  max = {maxi:5.1f}")
print(rang(etudiants, MATIERES))
ecrit_bulletins(etudiants, MATIERES, "bulletins.txt")
```

Pour le bonus, la moyenne pondérée s'écrit :

```python
def moyenne_ponderee(etudiant, coefficients):
    total = 0
    somme_coefs = 0
    for matiere, coef in coefficients.items():
        total += etudiant[matiere] * coef
        somme_coefs += coef
    return total / somme_coefs
```

Étape 8, avec `pandas` : le chargement, les moyennes et les statistiques par matière tiennent en quelques lignes.

```python
import pandas as pd

notes = pd.read_csv("donnees/notes.csv", sep=";")
notes["moyenne"] = notes[["maths", "info", "anglais"]].mean(axis=1)
print(notes[["maths", "info", "anglais"]].agg(["min", "mean", "max"]))
print(notes.sort_values("moyenne", ascending=False)[["prenom", "nom", "moyenne"]])
```
````

```{raw} latex
\fi
```


## Projet 2 : Les manchots de l'archipel Palmer ★★

_Chapitres mobilisés : 11 à 14._

On souhaite réaliser une étude descriptive du jeu de données `donnees/penguins.csv` (présenté au chapitre 11), puis répondre à une question : **peut-on reconnaître l'espèce d'un manchot à partir des seules mesures de son bec ?**

### Étapes

1. **Charger et décrire** : chargez les données, affichez leur taille, les types des colonnes et le nombre de valeurs manquantes par colonne.
2. **Nettoyer** : supprimez les lignes pour lesquelles les mesures du bec sont manquantes. Combien de manchots reste-t-il ?
3. **Résumer** : construisez un tableau donnant, pour chaque espèce, le nombre d'individus et la moyenne de chacune des quatre mesures, arrondie à une décimale.
4. **Visualiser** : tracez le nuage de points longueur du bec / épaisseur du bec, coloré par espèce. Décrivez les trois groupes que vous observez.
5. **Une règle de décision** : à partir du graphique, proposez une règle simple, sous la forme d'une fonction `devine_espece(longueur, epaisseur)` qui retourne `"Adelie"`, `"Chinstrap"` ou `"Gentoo"` à l'aide de deux seuils (par exemple : « si le bec est court, c'est un Adélie ; sinon, s'il est fin, c'est un Gentoo ; sinon c'est un Chinstrap »).
6. **Évaluer la règle** : ajoutez au tableau une colonne `prediction` contenant l'espèce devinée par votre fonction pour chaque manchot, puis calculez la proportion de manchots bien classés. Affichez le tableau croisé espèce réelle / espèce prédite : quelles erreurs votre règle commet-elle ?
7. **Modéliser la masse** : ajustez une régression linéaire de la masse sur la longueur de la nageoire, l'espèce et le sexe (chapitre 14). Quel est, à nageoire et espèce égales, l'écart de masse moyen entre mâles et femelles ? Vérifiez les résidus.
8. **Bonus** : essayez d'autres seuils pour améliorer votre taux de bonne classification. Est-ce une bonne idée de chercher les seuils « parfaits » pour ces données précises ? (Pensez à ce qui se passerait sur de nouveaux manchots.)

```{raw} latex
\iffalse
```

```{admonition} Indice pour l'étape 6
:class: hint, dropdown

Votre fonction prend deux arguments : on ne peut donc pas utiliser directement `df["colonne"].apply(...)`.
Le plus simple est d'utiliser une liste en compréhension avec `zip` (chapitre 5) :
`[devine_espece(l, e) for l, e in zip(df["bill_length_mm"], df["bill_depth_mm"])]`.
La proportion de bien classés est la moyenne du masque `df["prediction"] == df["species"]`.
```

````{admonition} Solution complète
:class: tip, dropdown

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Charger et décrire
df = pd.read_csv("donnees/penguins.csv")
print(df.shape)
print(df.dtypes)
print(df.isna().sum())

# 2. Nettoyer
df = df.dropna(subset=["bill_length_mm", "bill_depth_mm"])
print(len(df), "manchots")   # 342

# 3. Résumer
mesures = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
resume = df.groupby("species")[mesures].mean().round(1)
resume["effectif"] = df.groupby("species").size()
print(resume)

# 4. Visualiser
sns.scatterplot(data=df, x="bill_length_mm", y="bill_depth_mm", hue="species")
plt.show()
# Adélie : becs courts et épais ; Gentoo : becs longs et fins ; Chinstrap : becs longs et épais.

# 5. Une règle de décision
def devine_espece(longueur, epaisseur):
    if longueur < 42.5:
        return "Adelie"
    elif epaisseur < 16.5:
        return "Gentoo"
    else:
        return "Chinstrap"

# 6. Évaluer la règle
df["prediction"] = [devine_espece(l, e) for l, e in zip(df["bill_length_mm"], df["bill_depth_mm"])]
print((df["prediction"] == df["species"]).mean())   # environ 0.92
print(pd.crosstab(df["species"], df["prediction"]))

# 7. Modéliser la masse
import statsmodels.formula.api as smf
modele = smf.ols("body_mass_g ~ flipper_length_mm + C(species) + C(sex)", data=df.dropna()).fit()
print(modele.summary().tables[1])   # mâles : environ +530 g, à nageoire et espèce égales
plt.scatter(modele.fittedvalues, modele.resid, alpha=0.5)
plt.axhline(0, color="grey")
plt.show()
```

Avec deux seuils choisis « à l'œil », on reconnaît correctement l'espèce de plus de 9 manchots sur 10.
Le tableau croisé montre que les erreurs concernent surtout des Adélie au bec un peu long (classés Chinstrap) et des Gentoo au bec un peu épais (classés Chinstrap eux aussi) : ce sont les zones où les groupes se chevauchent sur le graphique.

Pour l'étape 8 : chercher les seuils qui donnent le meilleur résultat **sur ces données précises** risque de « coller » à leurs particularités, et la règle fonctionnerait moins bien sur de nouveaux manchots (on parle de **surapprentissage**).
C'est la question centrale de l'**apprentissage automatique** (_machine learning_), qui consiste à construire de telles règles automatiquement : la bibliothèque `scikit-learn` est l'outil de référence en Python pour cela.
````

```{raw} latex
\fi
```

## Projet 3 : Qui a survécu au naufrage du Titanic ? ★★★

_Chapitres mobilisés : 11 à 14._

Le 15 avril 1912, le Titanic sombre lors de son voyage inaugural. Le fichier `donnees/titanic.csv` décrit 891 de ses passagers (voir l'exercice 11.5).
L'objectif de ce projet est de produire une petite **étude**, sous la forme d'un notebook commenté, répondant à la question : **quels facteurs ont influencé les chances de survie ?**

### Étapes

1. **Découvrir les données** : taille, types, valeurs manquantes, statistiques descriptives. Quelle est la proportion de survivants ?
2. **Préparer les données** :
   - supprimez la colonne `deck`, trop incomplète ;
   - complétez les âges manquants par l'âge médian de la classe du passager (exercice 12.2) ;
   - créez une colonne `taille_famille` égale à `sibsp + parch + 1` (le passager, plus ses frères, sœurs et conjoint·e, plus ses parents et enfants à bord) ;
   - créez une colonne `tranche_age` (exercice 12.3).
3. **Analyser** : calculez le taux de survie selon le sexe, la classe, la tranche d'âge, le port d'embarquement et la taille de la famille. Présentez chaque résultat dans un petit tableau trié.
4. **Visualiser** : produisez une figure de 4 graphiques (une grille 2 × 2) qui résume vos principaux résultats.
5. **Modéliser** : ajustez une régression logistique de la survie sur le sexe, la classe, l'âge (complété) et la taille de la famille (chapitre 14). Présentez les _odds ratios_ et leurs intervalles de confiance. L'effet de la classe persiste-t-il à sexe et âge égaux ?
6. **Conclure** : rédigez, dans une cellule de texte, une conclusion de 5 à 10 lignes. Attention à ne pas confondre **corrélation** et **causalité** : par exemple, les passagers embarqués à Cherbourg ont-ils survécu davantage _parce qu'ils_ ont embarqué à Cherbourg ? (Indice : regardez la répartition des classes selon le port.)
7. **Exporter** : enregistrez le tableau préparé à l'étape 2 dans un fichier `titanic_prepare.csv`.

```{raw} latex
\iffalse
```

```{admonition} Indice pour l'étape 6
:class: hint, dropdown

`pd.crosstab(titanic["embark_town"], titanic["class"], normalize="index")` donne la répartition des classes pour chaque port.
```

````{admonition} Solution complète
:class: tip, dropdown

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Découvrir les données
titanic = pd.read_csv("donnees/titanic.csv")
print(titanic.shape)
print(titanic.isna().sum())
print(titanic.describe())
print("Proportion de survivants :", round(titanic["survived"].mean(), 3))   # 0.384

# 2. Préparer les données
titanic = titanic.drop(columns=["deck"])
medianes = titanic.groupby("pclass")["age"].median()
for classe in [1, 2, 3]:
    lignes = (titanic["pclass"] == classe) & titanic["age"].isna()
    titanic.loc[lignes, "age"] = medianes[classe]
titanic["taille_famille"] = titanic["sibsp"] + titanic["parch"] + 1
titanic["tranche_age"] = pd.cut(titanic["age"], bins=[0, 12, 18, 60, 100],
                                labels=["enfant", "adolescent", "adulte", "senior"])

# 3. Analyser
for colonne in ["sex", "class", "tranche_age", "embark_town", "taille_famille"]:
    taux = titanic.groupby(colonne, observed=True)["survived"].agg(["count", "mean"]).round(2)
    print(taux.sort_values("mean", ascending=False), "\n")

# 4. Visualiser
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
sns.barplot(data=titanic, x="sex", y="survived", ax=axes[0, 0])
axes[0, 0].set_title("Taux de survie selon le sexe")
sns.barplot(data=titanic, x="class", y="survived", hue="sex", ax=axes[0, 1])
axes[0, 1].set_title("Taux de survie selon la classe et le sexe")
sns.barplot(data=titanic, x="tranche_age", y="survived", ax=axes[1, 0])
axes[1, 0].set_title("Taux de survie selon l'âge")
sns.barplot(data=titanic, x="taille_famille", y="survived", ax=axes[1, 1])
axes[1, 1].set_title("Taux de survie selon la taille de la famille")
for ax in axes.ravel():
    ax.set_ylabel("Taux de survie")
fig.tight_layout()
plt.show()

# 5. Modéliser
import numpy as np
import statsmodels.formula.api as smf
logit = smf.logit("survived ~ C(sex) + C(pclass) + age + taille_famille", data=titanic).fit(disp=0)
print(logit.summary().tables[1])
odds_ratios = pd.DataFrame({
    "OR": np.exp(logit.params),
    "IC 2.5 %": np.exp(logit.conf_int()[0]),
    "IC 97.5 %": np.exp(logit.conf_int()[1]),
}).round(3)
print(odds_ratios)

# 6. Classes selon le port d'embarquement
print(pd.crosstab(titanic["embark_town"], titanic["class"], normalize="index").round(2))

# 7. Exporter
titanic.to_csv("titanic_prepare.csv", index=False)
```

Exemple de conclusion :

> Le sexe est le facteur le plus déterminant : 74 % des femmes ont survécu, contre 19 % des hommes. La classe joue aussi un rôle majeur (63 % de survivants en 1re classe contre 24 % en 3e), y compris à sexe égal : presque toutes les femmes de 1re et 2e classe ont survécu, contre la moitié de celles de 3e classe. Les enfants ont davantage survécu que les adultes. Les passagers voyageant seuls, ou avec une famille très nombreuse, ont eu moins de chances que ceux voyageant en petite famille.
> La régression logistique confirme ces effets « toutes choses égales par ailleurs » : à classe, âge et taille de famille égaux, la cote de survie d'un homme est environ 16 fois plus faible que celle d'une femme (_odds ratio_ de 0,06), et celle d'un passager de 3e classe environ 12 fois plus faible que celle d'un passager de 1re classe (0,08).
> Le taux de survie plus élevé des passagers embarqués à Cherbourg s'explique au moins en partie par la forte proportion de passagers de 1re classe parmi eux : le port d'embarquement est corrélé à la survie, mais n'en est probablement pas la cause.
````

```{raw} latex
\fi
```
