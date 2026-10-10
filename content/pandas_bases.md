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

(ch:pandas_bases)=
# Découvrir ses données avec `pandas`

```{code-cell}
:tags: [remove-cell]
# Réglage d'affichage pour la version PDF (cellule masquée)
import pandas as pd
pd.set_option("display.width", 70)
```

```{admonition} Objectifs du chapitre
:class: note

À la fin de ce chapitre, vous saurez :

* expliquer ce que sont un `DataFrame` et une `Series` ;
* charger un fichier CSV avec `pd.read_csv` (y compris un fichier « à la française ») ;
* obtenir une vue d'ensemble d'un jeu de données (`head`, `shape`, `info`, `describe`, `value_counts`) ;
* sélectionner des colonnes, filtrer des lignes et trier un tableau ;
* utiliser `loc` et `iloc`.

**Prérequis :** chapitres 1 à 10 (en particulier les listes, les dictionnaires et les masques `numpy`). **Durée indicative :** 2h30.
```

En analyse de données, on travaille presque toujours sur des **tableaux** : une ligne par individu observé (un étudiant, un client, une commune…) et une colonne par caractéristique mesurée (âge, revenu, population…).
La bibliothèque `pandas` est l'outil de référence en Python pour manipuler de tels tableaux : on peut la voir comme un **tableur programmable**, avec lequel chaque manipulation est écrite dans du code, et donc reproductible, vérifiable et réutilisable sur de nouvelles données.

```{admonition} Où travailler ?
:class: tip

À partir de ce chapitre, travaillez dans un **notebook Jupyter** (avec Anaconda, VS Code, ou en ligne sur Google Colab, voir l'introduction) : on y voit directement les tableaux et les graphiques sous chaque cellule de code, ce qui est idéal pour explorer des données.
Les fenêtres de code intégrées à la version web de ce document ne disposent pas de `pandas`.

Si `pandas` n'est pas installé, installez-le avec `pip install pandas` (il est inclus dans Anaconda et dans Google Colab).
```

Par convention, on importe `pandas` sous le nom `pd` :

```{code-cell}
import pandas as pd
```

````{admonition} Si vous venez de R ou de SAS
:class: seealso

Un `DataFrame` est l'équivalent d'un `data.frame` (ou d'un _tibble_) en R, et d'une table SAS. Voici les correspondances des opérations de ce chapitre :

| Opération | R (base / `dplyr`) | SAS | `pandas` |
|---|---|---|---|
| Lire un CSV | `read.csv("f.csv")`, `read.csv2` | `PROC IMPORT` | `pd.read_csv("f.csv")` (`sep=";"`, `decimal=","`) |
| Premières lignes | `head(df)` | `PROC PRINT (OBS=5)` | `df.head()` |
| Dimensions | `dim(df)`, `nrow(df)` | `PROC CONTENTS` | `df.shape`, `len(df)` |
| Structure | `str(df)` | `PROC CONTENTS` | `df.info()`, `df.dtypes` |
| Statistiques | `summary(df)` | `PROC MEANS` | `df.describe()` |
| Effectifs | `table(df$x)` | `PROC FREQ` | `df["x"].value_counts()` |
| Une colonne | `df$x`, `df[["x"]]` | | `df["x"]` |
| Plusieurs colonnes | `select(df, x, y)` | `KEEP x y;` | `df[["x", "y"]]` |
| Filtrer | `filter(df, x > 5 & y == "a")` | `WHERE x > 5 AND y = "a";` | `df[(df["x"] > 5) & (df["y"] == "a")]` |
| Trier | `arrange(df, desc(x))` | `PROC SORT; BY DESCENDING x;` | `df.sort_values("x", ascending=False)` |
| Valeur manquante | `NA`, `is.na(x)` | `.`, `MISSING(x)` | `NaN`, `df["x"].isna()` |

Deux différences importantes :

* les lignes d'un `DataFrame` ont un **index** (par défaut 0, 1, 2…), qui est conservé lors d'un filtre : après un filtre, les numéros de lignes ne sont donc plus consécutifs (utilisez `reset_index(drop=True)` pour les renuméroter) ;
* les colonnes se désignent par des **chaînes de caractères** (`df["x"]`), et non par des noms nus comme dans `dplyr` ou SAS.
````

## Le jeu de données de ce chapitre

Nous allons travailler sur un jeu de données réel, très utilisé pour apprendre l'analyse de données : les **manchots de l'archipel Palmer** (_Palmer penguins_), collectés en Antarctique par la Dr. Kristen Gorman entre 2007 et 2009 et diffusés librement.
Il décrit 344 manchots de trois espèces (Adélie, à jugulaire — _Chinstrap_ — et papou — _Gentoo_), vivant sur trois îles, avec pour chacun :

| Colonne | Signification |
|---|---|
| `species` | espèce |
| `island` | île |
| `bill_length_mm`, `bill_depth_mm` | longueur et épaisseur du bec (en mm) |
| `flipper_length_mm` | longueur de la nageoire (en mm) |
| `body_mass_g` | masse (en g) |
| `sex` | sexe (`MALE` ou `FEMALE`) |

Le fichier se trouve dans `donnees/penguins.csv`.

```{admonition} Si vous n'avez pas le fichier
:class: seealso

La bibliothèque `seaborn` (que nous utiliserons au chapitre 13) peut télécharger ce jeu de données pour vous : `import seaborn as sns` puis `df = sns.load_dataset("penguins")` (une connexion internet est nécessaire).
Le tableau obtenu est le même, aux majuscules près dans la colonne `sex` (`Male` / `Female`).
```

## `DataFrame` et `Series`

Chargeons le fichier avec la fonction `pd.read_csv` et affichons ses premières lignes avec la méthode `head` :

```{code-cell}
df = pd.read_csv("donnees/penguins.csv")
df.head()
```

```{admonition} Remarque
:class: seealso

Dans un notebook, la dernière expression d'une cellule est affichée automatiquement : c'est pourquoi on écrit simplement `df.head()` sans `print`.
Les tableaux sont alors joliment mis en forme. Dans un script `.py`, il faut écrire `print(df.head())`.
```

L'objet `df` est un **`DataFrame`** : un tableau à deux dimensions, dont chaque colonne a un nom et chaque ligne une étiquette (l'**index**, ici simplement les entiers 0, 1, 2…).
Chaque colonne, prise isolément, est une **`Series`** : une suite de valeurs du même type, accompagnée de l'index.

```{figure} ../img/fig_dataframe.*
:width: 95%

Anatomie d'un `DataFrame` (ici un extrait de 5 lignes et 4 colonnes du jeu de données).
```

```{code-cell}
masses = df["body_mass_g"]
print(type(df))
print(type(masses))
masses.head()
```

On peut aussi créer un `DataFrame` « à la main », à partir d'un dictionnaire associant à chaque nom de colonne la liste de ses valeurs :

```{code-cell}
petit = pd.DataFrame({
    "prenom": ["Aude", "Yanis", "Maëlle"],
    "maths": [14, 9, 16],
    "info": [17, 12, 13]
})
petit
```

```{admonition} À retenir
:class: important

* Un `DataFrame` est un tableau : **une ligne par observation, une colonne par variable**.
* Une colonne d'un `DataFrame` est une `Series`, que l'on obtient avec `df["nom_de_colonne"]`.
* Une `Series` ressemble à un tableau `numpy` à une dimension (on peut faire des calculs sur toute la colonne d'un coup, sans boucle), avec en plus un index.
```

## Charger un fichier CSV

`pd.read_csv` accepte de nombreux arguments pour s'adapter au format du fichier. Les plus utiles sont :

| Argument | Rôle | Exemple |
|---|---|---|
| `sep` | délimiteur des colonnes (par défaut `","`) | `sep=";"` |
| `decimal` | séparateur décimal (par défaut `"."`) | `decimal=","` |
| `encoding` | encodage du fichier (par défaut UTF-8) | `encoding="iso-8859-1"` |
| `index_col` | colonne à utiliser comme index | `index_col="prenom"` |
| `na_values` | valeurs à considérer comme manquantes | `na_values=["NA", "-"]` |

Les fichiers produits par un tableur réglé en français utilisent souvent le point-virgule comme délimiteur et la virgule comme séparateur décimal.
Le fichier `donnees/notes.csv`, déjà utilisé au chapitre 9, utilise des points-virgules :

```{code-cell}
notes = pd.read_csv("donnees/notes.csv", sep=";")
notes
```

Comparez avec le chapitre 9 : une seule ligne suffit à lire le fichier, et les notes sont **automatiquement converties en nombres** !

```{admonition} Erreur fréquente
:class: warning

Si vous oubliez `sep=";"` pour un fichier séparé par des points-virgules, `pandas` ne voit qu'**une seule colonne**, dont le nom est toute la ligne d'en-tête (`"nom;prenom;maths;info;anglais"`).
Premier réflexe après un chargement : **toujours regarder le résultat** avec `head()` et `shape`.
```

## Explorer un jeu de données

Avant toute analyse, il faut prendre connaissance des données : combien de lignes ? quelles colonnes ? quels types ? y a-t-il des valeurs manquantes ? Voici les outils de base.

### Dimensions et colonnes

```{code-cell}
print(df.shape)     # (nombre de lignes, nombre de colonnes) : un tuple
print(df.columns)   # noms des colonnes
```

Les méthodes `head(n)` et `tail(n)` affichent les `n` premières et dernières lignes (5 par défaut) ; `sample(n)` affiche `n` lignes tirées au hasard.

### Types et valeurs manquantes : `info`

```{code-cell}
df.info()
```

`info` indique, pour chaque colonne, le nombre de valeurs non manquantes (_non-null_) et le type des données : `float64` pour des nombres à virgule, `int64` pour des entiers, `object` ou `str` pour du texte.
On voit ici que le sexe n'est pas renseigné pour 11 manchots (333 valeurs sur 344), et que 2 manchots n'ont pas de mesures.
Dans `pandas`, une valeur manquante est notée `NaN` (_Not a Number_) ; nous verrons au chapitre suivant comment les traiter.

### Statistiques descriptives : `describe`

```{code-cell}
df.describe()
```

Pour chaque colonne numérique, `describe` donne le nombre de valeurs (`count`), la moyenne (`mean`), l'écart-type (`std`), le minimum, les quartiles (25 %, 50 % = médiane, 75 %) et le maximum.
C'est un excellent moyen de repérer des valeurs aberrantes (une masse négative, un âge de 300 ans…).

### Variables qualitatives : `value_counts` et `unique`

Pour une colonne contenant des catégories, on compte les effectifs de chaque modalité avec `value_counts` :

```{code-cell}
df["species"].value_counts()
```

```{code-cell}
print(df["island"].unique())    # les valeurs distinctes
print(df["island"].nunique())   # leur nombre
print(df["species"].value_counts(normalize=True))   # proportions plutôt qu'effectifs
```

### Calculs sur une colonne

Comme pour les tableaux `numpy`, les méthodes `mean`, `median`, `std`, `min`, `max`, `sum`… s'appliquent à toute une colonne (les valeurs manquantes sont automatiquement ignorées) :

```{code-cell}
print(df["body_mass_g"].mean())
print(df["body_mass_g"].median())
print(df["flipper_length_mm"].max())
```

```{admonition} Testez-vous
:class: hint

1. Quel est le type de `df.shape` ? Comment obtenir uniquement le nombre de lignes ?
2. Que retourne `df["species"]` ? Et `df["species"].value_counts()` ?
3. Pourquoi `df["sex"].mean()` n'a-t-il pas de sens ?
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

1. C'est un _tuple_ `(nombre de lignes, nombre de colonnes)` ; le nombre de lignes est `df.shape[0]` (on peut aussi utiliser `len(df)`).
2. `df["species"]` est une `Series` contenant l'espèce de chaque manchot ; `value_counts()` retourne une `Series` dont l'index est la liste des espèces et les valeurs leurs effectifs.
3. La colonne `sex` contient du texte (une variable qualitative) : on ne peut pas en calculer la moyenne (Python produit d'ailleurs une erreur). On utilisera plutôt `value_counts`.
```

```{raw} latex
\fi
```

## Sélectionner des colonnes

Nous l'avons vu : `df["nom"]` sélectionne **une** colonne et retourne une `Series`.
Pour sélectionner **plusieurs** colonnes, on donne une **liste** de noms (d'où les doubles crochets) ; on obtient alors un `DataFrame` :

```{code-cell}
df[["species", "body_mass_g"]].head(3)
```

```{admonition} Erreur fréquente
:class: warning

* `df["species", "island"]` (sans les doubles crochets) provoque une `KeyError` : `pandas` cherche une colonne dont le nom serait le _tuple_ `("species", "island")`.
* Un nom de colonne mal orthographié (majuscules, espaces, accents…) provoque aussi une `KeyError`. En cas de doute, affichez `df.columns`.
```

## Filtrer des lignes

### Avec un masque booléen

Le filtrage des lignes reprend exactement le principe des **masques** vus avec `numpy` : une comparaison appliquée à une colonne produit une `Series` de booléens, que l'on utilise ensuite entre crochets pour ne garder que les lignes où le masque vaut `True`.

```{figure} ../img/fig_filtre.*
:width: 95%

Filtrer les lignes d'un `DataFrame` avec un masque booléen.
```

```{code-cell}
masque = df["body_mass_g"] > 5500
print(masque.head())
lourds = df[masque]
print(len(lourds), "manchots de plus de 5,5 kg")
lourds.head()
```

On écrit généralement le filtre directement entre crochets : `df[df["body_mass_g"] > 5500]`.
Pour une colonne de texte, on teste l'égalité avec `==`, ou l'appartenance à une liste de valeurs avec la méthode `isin` :

```{code-cell}
adelie = df[df["species"] == "Adelie"]
print(adelie.shape)
deux_iles = df[df["island"].isin(["Dream", "Biscoe"])]
print(deux_iles.shape)
```

### Combiner des conditions

Pour combiner plusieurs conditions, on utilise **`&`** (et), **`|`** (ou) et **`~`** (non), en mettant **chaque condition entre parenthèses** :

```{code-cell}
femelles_gentoo = df[(df["species"] == "Gentoo") & (df["sex"] == "FEMALE")]
print(len(femelles_gentoo))
extremes = df[(df["body_mass_g"] < 3000) | (df["body_mass_g"] > 6000)]
extremes
```

```{admonition} À retenir
:class: important

Avec `pandas` (et `numpy`), on combine des masques avec `&`, `|` et `~`, **et non** avec `and`, `or` et `not` (qui provoquent l'erreur `ValueError: The truth value of a Series is ambiguous`).
Les parenthèses autour de chaque condition sont **obligatoires** : `df["a"] > 1 & df["b"] < 2` ne fait pas ce que l'on croit, car `&` est prioritaire sur `>`.
```

```{admonition} Testez-vous
:class: hint

Écrivez le filtre qui sélectionne :

1. les manchots de l'île Torgersen ;
2. les manchots dont la nageoire mesure au moins 200 mm, sauf ceux de l'espèce Gentoo ;
3. les manchots dont le sexe n'est pas renseigné (indice : la méthode `isna()` d'une `Series` retourne un masque).
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

1. `df[df["island"] == "Torgersen"]`
2. `df[(df["flipper_length_mm"] >= 200) & (df["species"] != "Gentoo")]` (ou `& ~(df["species"] == "Gentoo")`)
3. `df[df["sex"].isna()]`
```

```{raw} latex
\fi
```

## `loc` et `iloc`

Pour sélectionner à la fois des lignes **et** des colonnes, on utilise les accesseurs `loc` et `iloc`, avec la syntaxe `[lignes, colonnes]` :

* `df.loc[...]` sélectionne par **étiquettes** : noms des lignes (l'index) et noms des colonnes ;
* `df.iloc[...]` sélectionne par **positions** : numéros de lignes et de colonnes, comptés à partir de 0, comme pour les listes.

```{figure} ../img/fig_loc_iloc.*
:width: 85%

`loc` utilise les noms, `iloc` les positions.
```

```{code-cell}
notes = pd.read_csv("donnees/notes.csv", sep=";", index_col="prenom")
notes
```

```{code-cell}
print(notes.loc["Yanis", "info"])
print(notes.iloc[1, 2])
notes.loc[["Aude", "Inès"], ["maths", "info"]]
```

Ici, la colonne `nom` est la colonne de position 0 : la colonne `info` a donc la position 2 (contrairement au schéma, qui ne contient pas la colonne `nom`).

Comme pour les listes, on peut utiliser des tranches (`debut:fin`), et `:` seul signifie « tout ».
Attention : avec `loc`, la borne de fin est **incluse** (puisque l'on travaille avec des noms), alors qu'avec `iloc` elle est exclue :

```{code-cell}
notes.loc["Aude":"Maëlle", "maths":"info"]   # Maëlle et info inclus
```

```{code-cell}
notes.iloc[0:3, 1:3]   # lignes 0 à 2, colonnes 1 et 2
```

L'utilisation la plus fréquente de `loc` consiste à combiner un **filtre sur les lignes** et une **sélection de colonnes** :

```{code-cell}
notes.loc[notes["maths"] >= 14, ["nom", "maths"]]
```

## Trier

La méthode `sort_values` trie les lignes selon une ou plusieurs colonnes (ordre croissant par défaut) :

```{code-cell}
df.sort_values("body_mass_g", ascending=False).head(3)
```

```{code-cell}
# Tri selon l'espèce, puis par masse décroissante au sein de chaque espèce
df.sort_values(["species", "body_mass_g"], ascending=[True, False]).head()
```

Comme les méthodes des chaînes de caractères, la plupart des méthodes de `pandas` **ne modifient pas** le `DataFrame` : elles en retournent un nouveau.
Pour conserver le résultat, il faut l'affecter à une variable : `df_trie = df.sort_values(...)`.

## Exercices

```{admonition} Rappel
:class: tip

Ces exercices sont à faire dans un notebook Jupyter, avec le fichier `donnees/penguins.csv` (sauf mention contraire).
Commencez chaque notebook par `import pandas as pd` et `df = pd.read_csv("donnees/penguins.csv")`.
```

(ex11.1)=
```{admonition} Exercice 11.1 : Premier contact ★
1. Combien y a-t-il de manchots de chaque sexe ? Combien n'ont pas de sexe renseigné ?
2. Quelle est la longueur moyenne du bec ? La longueur minimale et maximale de la nageoire ?
3. Sur combien d'îles différentes les manchots ont-ils été observés ?
```

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

`value_counts` ignore les valeurs manquantes par défaut ; ajoutez l'argument `dropna=False` pour les compter aussi.
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

df = pd.read_csv("donnees/penguins.csv")
print(df["sex"].value_counts(dropna=False))   # 168 MALE, 165 FEMALE, 11 NaN
print(df["bill_length_mm"].mean())
print(df["flipper_length_mm"].min(), df["flipper_length_mm"].max())
print(df["island"].nunique())
```
````

```{raw} latex
\fi
```

(ex11.2)=
```{admonition} Exercice 11.2 : Filtres ★
1. Combien de manchots de l'espèce Adelie vivent sur l'île Dream ?
2. Affichez l'espèce, l'île et la masse des 5 manchots les plus légers.
3. Quelle est la masse moyenne des manchots Gentoo ? Et celle des mâles Gentoo ?
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

df = pd.read_csv("donnees/penguins.csv")

# 1.
print(len(df[(df["species"] == "Adelie") & (df["island"] == "Dream")]))   # 56

# 2.
print(df.sort_values("body_mass_g")[["species", "island", "body_mass_g"]].head(5))

# 3.
gentoo = df[df["species"] == "Gentoo"]
print(gentoo["body_mass_g"].mean())
print(gentoo[gentoo["sex"] == "MALE"]["body_mass_g"].mean())
# ou, en une seule sélection :
print(df.loc[(df["species"] == "Gentoo") & (df["sex"] == "MALE"), "body_mass_g"].mean())
```
````

```{raw} latex
\fi
```

(ex11.3)=
```{admonition} Exercice 11.3 : Le fichier de notes ★★
Chargez le fichier `donnees/notes.csv` dans un `DataFrame` (attention au délimiteur !), puis :

1. affichez les étudiants ayant plus de 15 en informatique ;
2. affichez le nom et le prénom des étudiants ayant au moins 10 dans **les trois** matières ;
3. affichez le tableau trié par note d'anglais décroissante.
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

notes = pd.read_csv("donnees/notes.csv", sep=";")
print(notes[notes["info"] > 15])
tous_admis = notes[(notes["maths"] >= 10) & (notes["info"] >= 10) & (notes["anglais"] >= 10)]
print(tous_admis[["nom", "prenom"]])
print(notes.sort_values("anglais", ascending=False))
```
````

```{raw} latex
\fi
```

(ex11.4)=
```{admonition} Exercice 11.4 : Comparer les espèces ★★
Sans utiliser de boucle explicite sur les lignes, mais en utilisant une boucle sur les **noms d'espèces** (obtenus avec `unique`), affichez pour chaque espèce son nombre d'individus, sa masse moyenne et la longueur moyenne de son bec, avec une décimale.
(Le chapitre suivant présentera un outil, `groupby`, qui fait cela en une ligne.)
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

df = pd.read_csv("donnees/penguins.csv")
for espece in df["species"].unique():
    sous_df = df[df["species"] == espece]
    print(f"{espece:<10} : {len(sous_df)} individus, "
          f"masse moyenne {sous_df['body_mass_g'].mean():.1f} g, "
          f"bec {sous_df['bill_length_mm'].mean():.1f} mm")
```
````

```{raw} latex
\fi
```

(ex11.5)=
```{admonition} Exercice 11.5 : Le Titanic ★★
Le fichier `donnees/titanic.csv` contient des informations sur 891 passagers du Titanic : `survived` (1 si le passager a survécu, 0 sinon), `pclass` (classe de 1 à 3), `sex`, `age`, `fare` (prix du billet), `embark_town` (port d'embarquement), etc.

1. Chargez le fichier et explorez-le (`shape`, `info`, `describe`). Quelles colonnes ont des valeurs manquantes ?
2. Combien de passagers ont survécu ? Quelle proportion cela représente-t-il ? (Astuce : quelle est la moyenne d'une colonne qui ne contient que des 0 et des 1 ?)
3. Quel est le taux de survie des femmes ? Des hommes ?
4. Quel était le prix moyen d'un billet en 1re classe ? En 3e classe ?
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

titanic = pd.read_csv("donnees/titanic.csv")
print(titanic.shape)
titanic.info()   # age, embarked, deck et embark_town ont des valeurs manquantes

print(titanic["survived"].sum())    # 342 survivants
print(titanic["survived"].mean())   # environ 0.38 : la moyenne d'une colonne de 0/1 est une proportion

print(titanic[titanic["sex"] == "female"]["survived"].mean())   # environ 0.74
print(titanic[titanic["sex"] == "male"]["survived"].mean())     # environ 0.19

print(titanic[titanic["pclass"] == 1]["fare"].mean())   # environ 84
print(titanic[titanic["pclass"] == 3]["fare"].mean())   # environ 13.7
```
````

```{raw} latex
\fi
```

## Bilan du chapitre

```{admonition} À retenir
:class: important

* `import pandas as pd` ; `df = pd.read_csv("fichier.csv", sep=";", decimal=",")`.
* Un `DataFrame` est un tableau (lignes = observations, colonnes = variables) ; une colonne `df["col"]` est une `Series`.
* Explorer : `head()`, `shape`, `columns`, `info()`, `describe()`, `value_counts()`, `unique()`, `nunique()`.
* Colonnes : `df["col"]` (une `Series`), `df[["col1", "col2"]]` (un `DataFrame`).
* Filtrer : `df[df["col"] > 10]` ; combiner avec `&`, `|`, `~` et des parenthèses ; `isin([...])`.
* `df.loc[lignes, colonnes]` (par noms, fin incluse), `df.iloc[lignes, colonnes]` (par positions, fin exclue).
* Trier : `df.sort_values("col", ascending=False)`.
```

Faites le point : êtes-vous capable de…

- charger un fichier CSV, y compris avec un délimiteur `;` ?
- décrire un jeu de données inconnu : taille, colonnes, types, valeurs manquantes, statistiques ?
- compter les effectifs d'une variable qualitative ?
- sélectionner les lignes vérifiant plusieurs conditions ?
- expliquer la différence entre `loc` et `iloc` ?
