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

(ch:pandas_transformer)=
# Préparer et résumer ses données avec `pandas`

```{code-cell}
:tags: [remove-cell]
# Réglage d'affichage pour la version PDF (cellule masquée)
import pandas as pd
pd.set_option("display.width", 70)
```

```{admonition} Objectifs du chapitre
:class: note

À la fin de ce chapitre, vous saurez :

* créer, transformer, renommer et supprimer des colonnes ;
* repérer et traiter les valeurs manquantes ;
* manipuler des colonnes de texte et de dates ;
* calculer des statistiques par groupe avec `groupby` et des tableaux croisés ;
* fusionner deux tableaux et enregistrer le résultat dans un fichier.

**Prérequis :** chapitre 11. **Durée indicative :** 2h30.
```

Dans la réalité, les données sont rarement prêtes à l'emploi : il faut créer de nouvelles variables, corriger des types, gérer des valeurs manquantes… avant de pouvoir calculer des résumés.
On dit souvent que cette phase de **préparation** occupe la plus grande partie du temps d'une analyse de données !

```{code-cell}
import pandas as pd
import numpy as np

df = pd.read_csv("donnees/penguins.csv")
```

````{admonition} Différences avec R et SAS
:class: seealso

| Opération | R (`dplyr`, `tidyr`) | SAS | `pandas` |
|---|---|---|---|
| Nouvelle colonne | `mutate(df, z = x / y)` | étape DATA : `z = x / y;` | `df["z"] = df["x"] / df["y"]` |
| Condition | `ifelse(x > 0, "a", "b")` | `IF x > 0 THEN ...; ELSE ...;` | `np.where(df["x"] > 0, "a", "b")` |
| Recoder | `recode(x, a = "A")` | `PROC FORMAT` | `df["x"].map({"a": "A"})` ou `replace` |
| Découper en classes | `cut(x, breaks = ...)` | `PROC FORMAT` + `PUT` | `pd.cut(df["x"], bins=[...])` |
| Renommer | `rename(df, new = old)` | `RENAME old = new;` | `df.rename(columns={"old": "new"})` |
| Supprimer une colonne | `select(df, -x)` | `DROP x;` | `df.drop(columns=["x"])` |
| Retirer les manquants | `na.omit`, `drop_na(df, x)` | `IF NOT MISSING(x);` | `df.dropna(subset=["x"])` |
| Résumer par groupe | `group_by(g) \|> summarise(m = mean(x))` | `PROC MEANS; CLASS g; VAR x;` | `df.groupby("g")["x"].mean()` |
| Tableau croisé | `table(a, b)` | `PROC FREQ; TABLES a*b;` | `pd.crosstab(df["a"], df["b"])` |
| Jointure | `left_join(a, b, by = "id")`, `merge` | `MERGE a b; BY id;` ou `PROC SQL` | `pd.merge(a, b, on="id", how="left")` |
| Empiler | `rbind`, `bind_rows` | `SET a b;` | `pd.concat([a, b])` |
| Format large | `pivot_wider` | `PROC TRANSPOSE` | `df.pivot(...)`, `df.pivot_table(...)` |
| Exporter | `write.csv` | `PROC EXPORT` | `df.to_csv("f.csv", index=False)` |

Contrairement à SAS (`MERGE ... BY`), il n'est pas nécessaire de trier les tables avant une jointure.
Et contrairement à l'opérateur `|>` (ou `%>%`) de R, on enchaîne les opérations `pandas` avec des points : `df.dropna().groupby("g")["x"].mean().round(1)`.
````

## Créer et modifier des colonnes

### Calculs sur des colonnes

Pour créer une nouvelle colonne, il suffit de lui affecter une valeur, comme pour une nouvelle clé de dictionnaire.
Les calculs entre colonnes se font **élément par élément**, comme avec `numpy`, sans boucle :

```{code-cell}
df["body_mass_kg"] = df["body_mass_g"] / 1000
df["bill_ratio"] = df["bill_length_mm"] / df["bill_depth_mm"]
df[["body_mass_g", "body_mass_kg", "bill_ratio"]].head(3)
```

Si la colonne existe déjà, son contenu est remplacé.

### Recoder des valeurs : `map` et `replace`

Pour remplacer des valeurs par d'autres (traduire des modalités, regrouper des catégories…), on utilise la méthode `map` avec un **dictionnaire** de correspondance :

```{code-cell}
traduction = {"Adelie": "Adélie", "Chinstrap": "à jugulaire", "Gentoo": "papou"}
df["espece"] = df["species"].map(traduction)
df[["species", "espece"]].sample(4, random_state=0)
```

Attention : avec `map`, une valeur absente du dictionnaire devient une valeur manquante. Pour ne remplacer que certaines valeurs et laisser les autres intactes, utilisez plutôt `replace` avec le même dictionnaire.

### Découper en classes : `pd.cut`

Pour transformer une variable numérique en catégories (des tranches d'âge, des classes de masse…), on utilise `pd.cut` en précisant les bornes des classes :

```{code-cell}
df["gabarit"] = pd.cut(df["body_mass_g"], bins=[0, 3500, 4500, 7000],
                       labels=["petit", "moyen", "grand"])
df["gabarit"].value_counts()
```

Par défaut, chaque intervalle est ouvert à gauche et fermé à droite : une masse de 3500 g est classée « petit ».

### Appliquer une fonction : `apply`

Pour des transformations plus complexes, on peut appliquer à chaque valeur d'une colonne une fonction que l'on a écrite soi-même, avec `apply` :

```{code-cell}
def categorie_bec(longueur):
    if longueur < 40:
        return "court"
    elif longueur < 48:
        return "moyen"
    return "long"

df["bec"] = df["bill_length_mm"].apply(categorie_bec)
df["bec"].value_counts()
```

```{admonition} Bonne pratique
:class: tip

`apply` est très souple mais plus lent que les opérations vectorisées (`+`, `/`, `map`, `pd.cut`…), car il appelle la fonction Python une fois par ligne.
Utilisez-le seulement quand il n'existe pas d'outil plus direct.
```

### Renommer et supprimer des colonnes

```{code-cell}
df = df.rename(columns={"bill_length_mm": "bec_long", "bill_depth_mm": "bec_epais"})
df = df.drop(columns=["body_mass_kg", "bill_ratio", "bec"])
df.columns
```

Comme `sort_values`, les méthodes `rename` et `drop` retournent un **nouveau** `DataFrame` : pour conserver le résultat, on le réaffecte à `df`.

## Les valeurs manquantes

Les valeurs manquantes (`NaN`) sont omniprésentes dans les données réelles : capteur en panne, question sans réponse, information inconnue…
Il faut toujours commencer par les **compter** :

```{code-cell}
df.isna().sum()
```

`isna()` produit un tableau de booléens (`True` là où la valeur manque), et `sum()` compte les `True` dans chaque colonne.

Plusieurs stratégies sont possibles :

* **supprimer** les lignes concernées, avec `dropna` (éventuellement en ne regardant que certaines colonnes grâce à l'argument `subset`) ;
* **remplacer** les valeurs manquantes par une valeur choisie, avec `fillna` (une valeur fixe, la moyenne ou la médiane de la colonne…).

```{code-cell}
complet = df.dropna(subset=["sex"])   # on retire les 11 manchots de sexe inconnu
print(df.shape, complet.shape)

df["sex"] = df["sex"].fillna("inconnu")
df["sex"].value_counts()
```

```{admonition} Attention
:class: warning

Aucune stratégie n'est neutre : supprimer des lignes réduit (et peut biaiser) l'échantillon, et remplacer par la moyenne invente des valeurs.
Le choix dépend de la question posée. Dans tous les cas, **notez ce que vous avez fait**, et vérifiez combien de lignes sont concernées.
```

```{admonition} Testez-vous
:class: hint

Après `df2 = df.dropna()`, combien de lignes reste-t-il si une seule colonne contient des valeurs manquantes, sur 10 lignes ? Et si deux colonnes contiennent chacune 2 valeurs manquantes, sur des lignes différentes ?
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

Sans argument, `dropna()` supprime toute ligne qui contient **au moins une** valeur manquante, dans n'importe quelle colonne.
Dans le premier cas, il reste 10 moins le nombre de valeurs manquantes de cette colonne. Dans le second, 4 lignes sont supprimées : il en reste 6.
C'est pourquoi on précise souvent `subset=[...]` pour ne tenir compte que des colonnes utiles à l'analyse.
```

```{raw} latex
\fi
```

## Texte et dates

### Les colonnes de texte : l'accesseur `.str`

Les méthodes des chaînes de caractères (`lower`, `upper`, `replace`, `startswith`…) s'appliquent à toute une colonne de texte grâce à l'accesseur `.str` :

```{code-cell}
df["sex"] = df["sex"].str.lower()
print(df["sex"].unique())
print(df["island"].str.upper().head(3))
print(df[df["island"].str.startswith("T")].shape)
```

La méthode `.str.contains("motif")` est particulièrement utile pour filtrer les lignes dont un texte contient un mot donné.

### Les dates : `pd.to_datetime` et l'accesseur `.dt`

Le fichier `donnees/flights.csv` contient le nombre mensuel de passagers (en milliers) d'une compagnie aérienne entre 1949 et 1960, un grand classique de l'étude des séries temporelles :

```{code-cell}
vols = pd.read_csv("donnees/flights.csv")
vols.head(3)
```

Pour exploiter les dates, il faut les convertir dans le type date de `pandas`, avec `pd.to_datetime`.
Ici, on construit d'abord une chaîne `"1949-January"`, puis on indique son format, à l’aide de codes : `%Y` pour l’année sur 4 chiffres, `%B` pour le nom du mois (en anglais) :

```{code-cell}
vols["date"] = pd.to_datetime(vols["year"].astype(str) + "-" + vols["month"], format="%Y-%B")
vols.dtypes
```

```{admonition} Formats de date courants
:class: seealso

* `pd.to_datetime("2024-10-10")` : le format international (année-mois-jour) est reconnu automatiquement ;
* pour des dates à la française (`"10/10/2024"`), précisez le format : `pd.to_datetime(colonne, format="%d/%m/%Y")` (ou l'argument `dayfirst=True`) ;
* `%d` jour, `%m` mois (numéro), `%Y` année sur 4 chiffres, `%H` heure, `%M` minutes.
```

Une fois convertie, une colonne de dates offre l'accesseur `.dt`, qui donne accès à l'année, au mois, au jour de la semaine… et on peut comparer ou soustraire des dates :

```{code-cell}
print(vols["date"].dt.year.head(3))
recents = vols[vols["date"] >= "1960-01-01"]
print(len(recents), "mois en 1960")
print(vols["date"].max() - vols["date"].min())
```

## Résumer par groupes : `groupby`

### Le principe

Une question revient sans cesse en analyse de données : « comment telle variable varie-t-elle **selon** telle catégorie ? » (la masse selon l'espèce, le taux de survie selon la classe, le salaire selon le diplôme…).
L'outil pour y répondre est `groupby`, qui suit le schéma « séparer, calculer, combiner » (_split-apply-combine_) :

```{figure} ../img/fig_groupby.*
:width: 98%

`groupby` sépare les lignes selon une colonne, calcule un résumé pour chaque groupe, puis rassemble les résultats.
```

```{code-cell}
df.groupby("species")["body_mass_g"].mean()
```

La syntaxe se lit ainsi : « grouper `df` par espèce, prendre la colonne de la masse, et en calculer la moyenne dans chaque groupe ».
Toutes les méthodes de résumé vues précédemment fonctionnent : `mean`, `median`, `std`, `min`, `max`, `sum`, `count`… ainsi que `size()`, qui compte le nombre de lignes de chaque groupe.

```{code-cell}
df.groupby("island").size()
```

### Plusieurs colonnes, plusieurs statistiques

On peut grouper selon **plusieurs** colonnes (en donnant une liste), et résumer plusieurs colonnes à la fois :

```{code-cell}
df.groupby(["species", "sex"])[["body_mass_g", "flipper_length_mm"]].mean().round(1)
```

La méthode `agg` permet de calculer plusieurs statistiques à la fois :

```{code-cell}
df.groupby("species")["body_mass_g"].agg(["count", "mean", "min", "max"])
```

Le résultat d'un `groupby` est un `DataFrame` (ou une `Series`) dont l'index est formé des groupes.
Pour retrouver un tableau « à plat », avec les groupes dans une colonne ordinaire, on ajoute `.reset_index()`.

### Tableaux croisés

Pour croiser deux variables qualitatives, `pd.crosstab` construit le tableau des effectifs (ou des proportions, avec l'argument `normalize`) :

```{code-cell}
pd.crosstab(df["species"], df["island"])
```

```{code-cell}
# Proportions par ligne : répartition de chaque espèce entre les îles
pd.crosstab(df["species"], df["island"], normalize="index").round(2)
```

```{admonition} Testez-vous
:class: hint

Que calculent les instructions suivantes ?

1. `df.groupby("island")["body_mass_g"].max()`
2. `df.groupby("species")["island"].nunique()`
3. `df.groupby("sex")["flipper_length_mm"].mean()["male"]`
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

1. La masse du manchot le plus lourd de chaque île.
2. Le nombre d'îles différentes sur lesquelles chaque espèce a été observée (Adélie : 3, Chinstrap : 1, Gentoo : 1).
3. La longueur moyenne de la nageoire des mâles (on sélectionne la valeur d'étiquette `"male"` dans la `Series` produite par `groupby`).
```

```{raw} latex
\fi
```

## Combiner des tableaux

### Fusionner : `merge`

Il arrive souvent que les informations soient réparties dans plusieurs tableaux, qui partagent une colonne commune (un identifiant, un nom…).
La fonction `pd.merge` les réunit, à la manière d'une jointure en base de données ou d'une RECHERCHEV dans un tableur :

```{code-cell}
infos_especes = pd.DataFrame({
    "species": ["Adelie", "Chinstrap", "Gentoo"],
    "nom_scientifique": ["Pygoscelis adeliae", "Pygoscelis antarcticus", "Pygoscelis papua"]
})
fusion = pd.merge(df, infos_especes, on="species", how="left")
fusion[["species", "nom_scientifique", "body_mass_g"]].head(3)
```

L'argument `how="left"` conserve toutes les lignes du premier tableau, même celles qui n'ont pas de correspondance dans le second (elles reçoivent alors des valeurs manquantes).

### Empiler : `concat`

Pour mettre bout à bout des tableaux ayant les mêmes colonnes (par exemple des données de plusieurs années stockées dans plusieurs fichiers), on utilise `pd.concat` :

```{code-cell}
debut = vols[vols["year"] == 1949]
fin = vols[vols["year"] == 1960]
pd.concat([debut, fin]).shape
```

## Enregistrer le résultat

Enfin, on enregistre un `DataFrame` dans un fichier CSV avec la méthode `to_csv` (l'argument `index=False` évite d'écrire l'index comme une colonne supplémentaire) :

```{code-cell}
resume = df.groupby("species")["body_mass_g"].mean().round(1).reset_index()
resume.to_csv("resume_especes.csv", index=False)
print(open("resume_especes.csv", encoding="utf-8").read())
```

Pour un fichier destiné à un tableur réglé en français, on peut utiliser `sep=";"` et `decimal=","`.
La méthode `to_excel("fichier.xlsx", index=False)` produit directement un fichier Excel (elle nécessite le paquet `openpyxl`) ; symétriquement, `pd.read_excel` lit un fichier Excel.

```{admonition} Erreurs fréquentes de ce chapitre
:class: warning

| Symptôme / message | Cause probable |
|---|---|
| La colonne créée ou modifiée « disparaît » | le résultat de `rename`, `drop`, `fillna`, `sort_values`… n'a pas été réaffecté (`df = df.drop(...)`) |
| Une colonne entière de `NaN` après `map` | les valeurs de la colonne ne correspondent pas exactement aux clés du dictionnaire (majuscules, espaces…) |
| `TypeError: unsupported operand type(s)` lors d'un calcul | la colonne est lue comme du texte (`object` ou `str`) : vérifier `df.dtypes`, convertir avec `pd.to_numeric(df["col"], errors="coerce")` |
| `ValueError: time data ... doesn't match format` | le format passé à `pd.to_datetime` ne correspond pas aux données |
| Une moyenne de groupe inattendue | des valeurs manquantes, des doublons ou des modalités mal orthographiées (`"Male"` / `"male"`) : vérifier avec `value_counts()` |
```

## Exercices

```{admonition} Rappel
:class: tip

Ces exercices utilisent le fichier `donnees/titanic.csv` (voir l'exercice 11.5 pour la description des colonnes).
Commencez votre notebook par `import pandas as pd` et `titanic = pd.read_csv("donnees/titanic.csv")`.
```

(ex12.1)=
```{admonition} Exercice 12.1 : Survie par groupe ★
1. Calculez le taux de survie selon le sexe, puis selon la classe (`class`), avec `groupby`.
2. Calculez le taux de survie selon le sexe **et** la classe. Quel groupe a le taux de survie le plus élevé ? Le plus faible ?
3. Construisez le tableau croisé des effectifs du sexe et de la classe.
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

titanic = pd.read_csv("donnees/titanic.csv")
print(titanic.groupby("sex")["survived"].mean())
print(titanic.groupby("class")["survived"].mean())

survie = titanic.groupby(["sex", "class"])["survived"].mean()
print(survie.sort_values())   # le plus élevé : femmes de 1re classe (97 %) ; le plus faible : hommes de 3e classe (14 %)

print(pd.crosstab(titanic["sex"], titanic["class"]))
```
````

```{raw} latex
\fi
```

(ex12.2)=
```{admonition} Exercice 12.2 : Les âges manquants ★★
1. Combien de passagers n'ont pas d'âge renseigné ? Quelle proportion cela représente-t-il ?
2. Calculez l'âge médian des passagers selon leur classe.
3. Créez une colonne `age_complete` dans laquelle les âges manquants sont remplacés par l'âge médian **de la classe du passager**.
```

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Pour la question 3, une approche simple consiste à traiter les trois classes l'une après l'autre : pour chaque classe, sélectionnez avec `loc` les lignes de cette classe dont l'âge est manquant, et affectez-leur la médiane calculée à la question 2.
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

titanic = pd.read_csv("donnees/titanic.csv")
print(titanic["age"].isna().sum())    # 177
print(titanic["age"].isna().mean())   # environ 20 %

medianes = titanic.groupby("pclass")["age"].median()
print(medianes)   # 37 ans en 1re classe, 29 en 2e, 24 en 3e

titanic["age_complete"] = titanic["age"]
for classe in [1, 2, 3]:
    lignes = (titanic["pclass"] == classe) & titanic["age"].isna()
    titanic.loc[lignes, "age_complete"] = medianes[classe]
print(titanic["age_complete"].isna().sum())   # 0
```

Pour aller plus loin : `pandas` permet d'écrire la question 3 en une ligne, avec `transform`, qui renvoie pour chaque ligne la statistique de son groupe :
`titanic["age"].fillna(titanic.groupby("pclass")["age"].transform("median"))`.
````

```{raw} latex
\fi
```

(ex12.3)=
```{admonition} Exercice 12.3 : Enfants et adultes ★★
1. Avec `pd.cut`, créez une colonne `tranche_age` découpant l'âge en quatre classes : « enfant » (de 0 à 12 ans), « adolescent » (12 à 18 ans), « adulte » (18 à 60 ans) et « senior » (plus de 60 ans).
2. Calculez le nombre de passagers et le taux de survie de chaque tranche d'âge.
3. Le principe « les femmes et les enfants d'abord » semble-t-il avoir été appliqué ?
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

titanic = pd.read_csv("donnees/titanic.csv")
titanic["tranche_age"] = pd.cut(titanic["age"], bins=[0, 12, 18, 60, 100],
                                labels=["enfant", "adolescent", "adulte", "senior"])
print(titanic.groupby("tranche_age", observed=True)["survived"].agg(["count", "mean"]))
```

Les enfants ont un taux de survie (environ 58 %) nettement supérieur à celui des adultes (environ 39 %), et les femmes (74 %) bien supérieur à celui des hommes (19 %) : le principe semble avoir été largement appliqué, même si la classe a aussi joué un rôle important (exercice 12.1).

L'argument `observed=True` indique à `pandas` de n'afficher que les catégories effectivement présentes ; il évite un avertissement avec les colonnes produites par `pd.cut`.
````

```{raw} latex
\fi
```

(ex12.4)=
```{admonition} Exercice 12.4 : Rapport par port d'embarquement ★★
Produisez un tableau qui donne, pour chaque port d'embarquement (`embark_town`), le nombre de passagers, l'âge moyen, le prix moyen du billet et le taux de survie (arrondis à 2 décimales), trié par nombre de passagers décroissant, puis enregistrez-le dans un fichier `rapport_ports.csv` lisible par un tableur français.
```

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

`agg` accepte aussi un dictionnaire associant à chaque colonne la statistique voulue : `.agg({"age": "mean", "fare": "mean", "survived": "mean"})`. Pour le nombre de passagers, utilisez par exemple `"count"` sur la colonne `survived`, dans un second `groupby`, ou la syntaxe d'agrégation nommée de la solution.
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

titanic = pd.read_csv("donnees/titanic.csv")
rapport = titanic.groupby("embark_town").agg(
    nb_passagers=("survived", "count"),
    age_moyen=("age", "mean"),
    prix_moyen=("fare", "mean"),
    taux_survie=("survived", "mean"),
).round(2).sort_values("nb_passagers", ascending=False)
print(rapport)
rapport.to_csv("rapport_ports.csv", sep=";", decimal=",")
```

Ici, on garde l'index (le nom du port) dans le fichier : on n'utilise donc pas `index=False`.
La syntaxe `nom_de_colonne=("colonne", "statistique")` (dite « agrégation nommée ») permet de choisir directement le nom des colonnes du résultat.
````

```{raw} latex
\fi
```

(ex12.5)=
```{admonition} Exercice 12.5 : Saisonnalité du trafic aérien ★★
Avec le fichier `donnees/flights.csv` :

1. calculez le nombre total de passagers par année ;
2. calculez le nombre moyen de passagers pour chaque mois de l'année (toutes années confondues). Quel est le mois le plus chargé ? Le moins chargé ?
3. de combien de pourcents le trafic annuel a-t-il augmenté entre 1949 et 1960 ?
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd

vols = pd.read_csv("donnees/flights.csv")
par_an = vols.groupby("year")["passengers"].sum()
print(par_an)

par_mois = vols.groupby("month")["passengers"].mean().sort_values()
print(par_mois)   # le plus chargé : July ; le moins chargé : November

augmentation = (par_an[1960] - par_an[1949]) / par_an[1949] * 100
print(f"Augmentation : {augmentation:.0f} %")   # environ 276 %
```
````

```{raw} latex
\fi
```

## Bilan du chapitre

```{admonition} À retenir
:class: important

* Nouvelle colonne : `df["c"] = df["a"] / df["b"]` ; recodage : `map(dico)`, `replace(dico)` ; classes : `pd.cut(col, bins=[...], labels=[...])` ; fonction : `apply(f)`.
* `rename(columns={...})`, `drop(columns=[...])` : penser à réaffecter le résultat.
* Valeurs manquantes : `isna().sum()`, `dropna(subset=[...])`, `fillna(valeur)`.
* Texte : `df["col"].str.lower()`, `.str.contains(...)` ; dates : `pd.to_datetime(..., format=...)`, `.dt.year`.
* Par groupe : `df.groupby("cat")["num"].mean()`, `.size()`, `.agg([...])` ; `pd.crosstab(a, b)`.
* Combiner : `pd.merge(df1, df2, on="cle", how="left")`, `pd.concat([df1, df2])` ; enregistrer : `df.to_csv("f.csv", index=False)`.
```

Faites le point : êtes-vous capable de…

- créer une variable calculée ou une variable en classes ?
- compter et traiter les valeurs manquantes d'un tableau ?
- convertir une colonne en dates et en extraire l'année ou le mois ?
- calculer une moyenne ou un effectif par groupe, selon une ou deux variables ?
- fusionner deux tableaux qui partagent une colonne ?
- enregistrer un tableau de résultats dans un fichier CSV ?
