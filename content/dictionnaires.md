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

(ch:dictionnaires)=
# Dictionnaires, _tuples_ et _sets_

```{admonition} Objectifs du chapitre
:class: note

À la fin de ce chapitre, vous saurez :

* créer un dictionnaire et y associer des valeurs à des clés ;
* lire, ajouter, modifier et supprimer des entrées ;
* parcourir un dictionnaire par clés, par valeurs ou par couples clé/valeur ;
* utiliser un dictionnaire pour compter des occurrences ;
* utiliser des _tuples_ (et les « déballer » dans plusieurs variables) et des _sets_ ;
* choisir entre une liste, un dictionnaire, un _tuple_ et un _set_.

**Prérequis :** chapitres 1 à 6. **Durée indicative :** 2h.
```

Comme une liste, un dictionnaire est une collection de données.
Mais au lieu de repérer chaque valeur par une position (un indice entier), on la repère par une **clé**, que l'on choisit librement.
Chaque entrée d'un dictionnaire est donc une association entre une **clé** et une **valeur**, comme dans un dictionnaire papier où l'on associe une définition à chaque mot.

On utilise souvent des chaînes de caractères comme clés : par exemple, pour représenter le stock d'un primeur, on associe à chaque nom de fruit le nombre de fruits disponibles.

```{figure} ../img/fig_dictionnaire.*
:width: 65%

Un dictionnaire associe des **valeurs** à des **clés**. On accède à une valeur grâce à sa clé.
```

Les clés sont des valeurs quelconques (non modifiables : des chaînes, des nombres…), la seule contrainte étant qu’**une même clé ne peut apparaître qu'une fois** dans un dictionnaire.

## Créer un dictionnaire

Pour définir un dictionnaire, on écrit ses paires `clé: valeur` entre accolades, séparées par des virgules :

```{code-cell}
stock = {"pomme": 3, "kiwi": 12, "poire": 0}
print(stock)
```

Un dictionnaire vide se crée avec des accolades vides :

```{code-cell}
mon_dico = {}
print(mon_dico)
print(len(stock))   # nombre de paires clé/valeur
```

## Lire le contenu d'un dictionnaire

Pour lire la valeur associée à une clé, on utilise la même syntaxe que pour les listes, en remplaçant l'indice par la clé :

```{code-cell}
stock = {"pomme": 3, "kiwi": 12, "poire": 0}
print(stock["kiwi"])
```

Si la clé demandée n'existe pas, on obtient une erreur `KeyError` :

```{code-cell}
:tags: [raises-exception]
print(stock["banane"])
```

Pour éviter cela, on peut d'abord tester si la clé est présente avec le mot-clé `in` (qui teste la présence d'une **clé**, et non d'une valeur) :

```{code-cell}
if "banane" in stock:
    print(stock["banane"])
else:
    print("Pas de bananes")
```

ou bien utiliser la méthode `get`, qui permet de préciser une valeur par défaut à retourner si la clé n'existe pas :

```{code-cell}
print(stock.get("kiwi", 0))
print(stock.get("banane", 0))
```

## Modifier le contenu d'un dictionnaire

Pour modifier la valeur associée à une clé, on utilise la même syntaxe que pour les listes :

```{code-cell}
stock = {"pomme": 3, "kiwi": 12, "poire": 0}
stock["pomme"] = 10
print(stock)
```

Et si la clé n'existe pas encore, la même syntaxe **crée** une nouvelle paire clé/valeur (contrairement aux listes, pour lesquelles un indice trop grand provoque une erreur) :

```{code-cell}
stock["banane"] = 6
print(stock)
```

Enfin, pour supprimer une paire clé/valeur, on utilise le mot-clé `del` :

```{code-cell}
del stock["poire"]
print(stock)
```

```{admonition} Testez-vous
:class: hint

Que contient `d` à la fin de ce programme ? Qu'affiche-t-il ?

    d = {"a": 1, "b": 2}
    d["c"] = 3
    d["a"] = d["a"] + 10
    del d["b"]
    print(len(d), d.get("b", "absent"), "c" in d, 3 in d)
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

`d` vaut `{"a": 11, "c": 3}` et le programme affiche :

    2 absent True False

`3 in d` vaut `False` car `in` teste la présence d'une **clé**, et 3 n'est pas une clé de `d` (c'est une valeur).
```

```{raw} latex
\fi
```

## Parcourir un dictionnaire

Comme pour les listes, il existe trois façons de parcourir un dictionnaire.

### Parcours par clés

Pour parcourir les clés, on utilise la méthode `keys` (ou, plus simplement, on parcourt directement le dictionnaire, ce qui revient au même) :

```{code-cell}
stock = {"pomme": 3, "kiwi": 12, "poire": 0}
for fruit in stock.keys():
    print(fruit)
```

### Parcours par valeurs

Pour parcourir uniquement les valeurs, on utilise la méthode `values` :

```{code-cell}
for quantite in stock.values():
    print(quantite)
```

### Parcours par couples clé/valeur

Pour accéder simultanément aux clés et aux valeurs associées, on utilise la méthode `items` :

```{code-cell}
for fruit, quantite in stock.items():
    print(f"{fruit} : {quantite}")
```

```{admonition} À propos de l'ordre
:class: seealso

Depuis Python 3.7, les dictionnaires conservent l'ordre dans lequel les clés ont été insérées, et c'est dans cet ordre qu'ils sont parcourus.
Mais ils ne sont pas pour autant « ordonnés » au sens des listes : il n'y a pas de « premier élément » accessible par `d[0]`.
Pour que votre code soit clair, évitez de faire reposer sa logique sur l'ordre des clés d'un dictionnaire.
```

## Exemple guidé : compter des occurrences

Une utilisation très fréquente des dictionnaires est le **comptage** : combien de fois chaque mot apparaît-il dans un texte ? combien d'étudiants ont obtenu chaque note ?
Comptons les votes d'un sondage :

```{code-cell}
votes = ["pizza", "sushi", "pizza", "crêpes", "pizza", "crêpes"]

compteurs = {}
for vote in votes:
    if vote in compteurs:
        compteurs[vote] += 1     # on a déjà vu ce vote : on incrémente
    else:
        compteurs[vote] = 1      # première fois : on crée l'entrée
print(compteurs)
```

Le schéma est toujours le même : si la clé existe déjà, on met à jour sa valeur ; sinon, on la crée.
Avec la méthode `get`, on peut même écrire les deux cas en une seule ligne : `compteurs[vote] = compteurs.get(vote, 0) + 1`.

*[Voir ce code s'exécuter pas à pas dans Python Tutor](https://pythontutor.com/visualize.html#code=votes%20%3D%20%5B%22pizza%22%2C%20%22sushi%22%2C%20%22pizza%22%2C%20%22cr%C3%AApes%22%2C%20%22pizza%22%2C%20%22cr%C3%AApes%22%5D%0A%0Acompteurs%20%3D%20%7B%7D%0Afor%20vote%20in%20votes%3A%0A%20%20%20%20if%20vote%20in%20compteurs%3A%0A%20%20%20%20%20%20%20%20compteurs%5Bvote%5D%20%2B%3D%201%20%20%20%20%20%23%20on%20a%20d%C3%A9j%C3%A0%20vu%20ce%20vote%20%3A%20on%20incr%C3%A9mente%0A%20%20%20%20else%3A%0A%20%20%20%20%20%20%20%20compteurs%5Bvote%5D%20%3D%201%20%20%20%20%20%20%23%20premi%C3%A8re%20fois%20%3A%20on%20cr%C3%A9e%20l%27entr%C3%A9e%0Aprint%28compteurs%29%0A&cumulative=false&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D&textReferences=false)*

## Des valeurs plus riches

Les valeurs d'un dictionnaire peuvent être de n'importe quel type, y compris des listes ou d'autres dictionnaires.
Cela permet de représenter des données structurées :

```{code-cell}
notes = {
    "Aude": [12, 15, 17],
    "Ali": [9, 14],
    "Chloé": [16, 13, 18, 11]
}
for prenom, liste_notes in notes.items():
    moyenne = sum(liste_notes) / len(liste_notes)
    print(f"{prenom} : moyenne de {moyenne:.2f} sur {len(liste_notes)} notes")
```

```{code-cell}
etudiant = {
    "nom": "Martin",
    "prenom": "Aude",
    "date_de_naissance": {"jour": 1, "mois": 6, "annee": 2005}
}
print(etudiant["date_de_naissance"]["annee"])
```

Nous retrouverons ce type de structure au chapitre 9, avec les fichiers JSON.

````{admonition} Liste ou dictionnaire ?
:class: tip

Lorsque l'on doit stocker une série de valeurs, on a donc le choix entre une liste et un dictionnaire.

On utilise un **dictionnaire** dès lors que l'on veut mettre en évidence une **correspondance entre des clés et des valeurs**, comme dans l'exemple suivant, dans lequel on associe à chaque numéro étudiant un entier (pouvant représenter une note, un nombre de photocopies restantes autorisées, ou autre) :

```
{"2170000": 13, "2180000": 23}
```

On utilise une **liste** pour stocker une **série ordonnée de valeurs**, comme une liste de prénoms :

```
["Chloé", "Ali", "Margot", "Antoine"]
```
````


````{admonition} Différences avec R et SAS
:class: seealso

* Un dictionnaire ressemble à une **liste nommée** de R (`list(pomme = 3, kiwi = 12)`, avec un accès `stock[["kiwi"]]`), ou à un format SAS (`PROC FORMAT`) qui associe des libellés à des codes.
* Avec `pandas`, les dictionnaires servent souvent à créer des tableaux (`pd.DataFrame({...})`, chapitre 11) et à recoder des valeurs (méthode `map`, chapitre 12).
````

## Deux autres collections : les _tuples_ et les _sets_

Pour terminer ce chapitre, voyons rapidement deux autres types de collections, que vous croiserez régulièrement (notamment avec `pandas`).

### Les _tuples_

Un _tuple_ s'écrit comme une liste, mais avec des parenthèses (facultatives) au lieu des crochets.
Il ressemble en de nombreux points à une liste (accès par indice, `len`, boucle `for`…), à une différence majeure près : **un _tuple_ ne peut pas être modifié** une fois créé.

```{code-cell}
point = (3, 7)
print(point[0], len(point))
```

```{code-cell}
:tags: [raises-exception]
point[0] = 5
```

Vous en avez déjà rencontré sans le savoir : quand une fonction retourne plusieurs valeurs séparées par des virgules (`return quotient, reste`), elle retourne en fait un _tuple_.
On peut répartir les valeurs d'un _tuple_ dans plusieurs variables en une seule instruction (on parle de **déballage**) :

```{code-cell}
x, y = point
print(x, y)
```

C'est ce qui se passe dans `for cle, valeur in d.items()` : à chaque tour, `items` fournit un _tuple_ `(clé, valeur)`, déballé dans deux variables.
Le déballage permet aussi d'échanger deux variables très simplement :

```{code-cell}
a, b = 5, 8
a, b = b, a
print(a, b)
```

Avec `pandas`, vous verrez par exemple que la taille d'un tableau de données est un _tuple_ `(nombre de lignes, nombre de colonnes)`.

### Les _sets_

Un _set_ (ou **ensemble**) est une collection **sans ordre et sans doublon**, notée avec des accolades comme les dictionnaires, mais sans valeurs associées.
Son utilisation la plus courante consiste à **éliminer les doublons** d'une liste, ou à connaître les **valeurs distinctes** d'une série de données :

```{code-cell}
villes = ["Rennes", "Brest", "Rennes", "Vannes", "Brest", "Rennes"]
distinctes = set(villes)
print(distinctes)
print(len(distinctes), "villes différentes")
```

On peut ajouter un élément avec `add`, tester l'appartenance avec `in`, et calculer intersections (`&`), unions (`|`) et différences (`-`) :

```{code-cell}
a = {1, 2, 3, 4}
b = {3, 4, 5}
print(a & b, a | b, a - b)
```

Attention : `{}` crée un dictionnaire vide ; un _set_ vide s'écrit `set()`.

### Récapitulatif

```{figure} ../img/fig_collections.*
:width: 95%

Les quatre types de collections de base en Python.
```

```{admonition} Testez-vous
:class: hint

Quelle structure utiliseriez-vous pour stocker :

1. les températures relevées chaque heure pendant une journée ?
2. la population de chaque commune de Bretagne ?
3. la position (latitude, longitude) d'une ville ?
4. la liste des espèces d'oiseaux observées au moins une fois (sans répétition) ?
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

1. Une **liste** : une série ordonnée de valeurs.
2. Un **dictionnaire** : on associe une valeur (la population) à une clé (le nom de la commune).
3. Un **_tuple_** : deux valeurs qui vont ensemble et ne changent pas.
4. Un **_set_** : on ne veut pas de doublons et l'ordre n'a pas d'importance.
```

```{raw} latex
\fi
```

## Exercices

(ex7.1)=
```{admonition} Exercice 7.1 : Somme des valeurs ★
Écrivez une fonction qui retourne la somme des **valeurs** d'un dictionnaire fourni en argument, en supposant que toutes ces valeurs soient numériques.
```

<div id="pad_7_1" class="pad"></div>
<script>
    Pythonpad('pad_7_1', {'id': 'aude_7.1', 'title': 'Testez votre code ici', 'src': "def somme_valeurs(d):\n    # Complétez ce code\n    pass\n\nprint(somme_valeurs({\"a\": 12, \"zz\": 1.5, \"AAA\": 0}))  # doit afficher 13.5\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
def somme_valeurs(d):
    s = 0
    for v in d.values():
        s += v
    return s

print(somme_valeurs({"a": 12, "zz": 1.5, "AAA": 0}))
```

On aurait aussi pu écrire `return sum(d.values())`.
````

```{raw} latex
\fi
```

(ex7.2)=
````{admonition} Exercice 7.2 : Occurrences des mots ★★
Écrivez une fonction qui compte le nombre d'occurrences de chacun des mots d'une chaîne de caractères et retourne le résultat sous forme de dictionnaire :

```
print(compte_occurrences("la vie est belle c'est la vie"))
# Doit afficher : {'la': 2, 'vie': 2, 'est': 1, 'belle': 1, "c'est": 1}
```
````

<div id="pad_7_2" class="pad"></div>
<script>
    Pythonpad('pad_7_2', {'id': 'aude_7.2', 'title': 'Testez votre code ici', 'src': "def compte_occurrences(s):\n    # Complétez ce code\n    pass\n\nprint(compte_occurrences(\"la vie est belle c'est la vie\"))\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Découpez la chaîne en mots avec `split`, puis reprenez le principe de l'exemple guidé sur les votes.
```

````{admonition} Solution
:class: tip, dropdown

```python
def compte_occurrences(s):
    d = {}
    for mot in s.split():
        d[mot] = d.get(mot, 0) + 1
    return d

print(compte_occurrences("la vie est belle c'est la vie"))
```
````

```{raw} latex
\fi
```

(ex7.3)=
```{admonition} Exercice 7.3 : Le mot le plus fréquent ★★
Écrivez une fonction `plus_frequent(d)` qui prend en argument un dictionnaire de comptages (comme celui retourné par la fonction de l'exercice précédent) et retourne la clé associée à la plus grande valeur.
```

<div id="pad_7_3" class="pad"></div>
<script>
    Pythonpad('pad_7_3', {'id': 'aude_7.3', 'title': 'Testez votre code ici', 'src': "def plus_frequent(d):\n    # Complétez ce code\n    pass\n\nprint(plus_frequent({\"pizza\": 3, \"sushi\": 1, \"crêpes\": 2}))  # doit afficher pizza\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

C'est la même idée que l'argmax d'une liste (exercice 5.1), mais en parcourant les couples clé/valeur avec `items`.
```

````{admonition} Solution
:class: tip, dropdown

```python
def plus_frequent(d):
    cle_max = None
    valeur_max = None
    for cle, valeur in d.items():
        if valeur_max is None or valeur > valeur_max:
            cle_max = cle
            valeur_max = valeur
    return cle_max

print(plus_frequent({"pizza": 3, "sushi": 1, "crêpes": 2}))
```

L'utilisation de `None` comme valeur initiale permet de gérer proprement le premier tour de boucle (et le cas du dictionnaire vide, pour lequel la fonction retourne `None`).
````

```{raw} latex
\fi
```

(ex7.4)=
```{admonition} Exercice 7.4 : Annuaire inversé ★★
On dispose d'un annuaire sous forme de dictionnaire associant à chaque nom un numéro de téléphone.
Écrivez une fonction `inverse_annuaire(annuaire)` qui retourne un nouveau dictionnaire associant à chaque numéro le nom correspondant.
```

<div id="pad_7_4" class="pad"></div>
<script>
    Pythonpad('pad_7_4', {'id': 'aude_7.4', 'title': 'Testez votre code ici', 'src': "def inverse_annuaire(annuaire):\n    # Complétez ce code\n    pass\n\nannuaire = {\"Aude\": \"0601020304\", \"Ali\": \"0605060708\"}\nprint(inverse_annuaire(annuaire))\n# doit afficher {'0601020304': 'Aude', '0605060708': 'Ali'}\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
def inverse_annuaire(annuaire):
    inverse = {}
    for nom, numero in annuaire.items():
        inverse[numero] = nom
    return inverse

annuaire = {"Aude": "0601020304", "Ali": "0605060708"}
print(inverse_annuaire(annuaire))
```

Que se passe-t-il si deux personnes partagent le même numéro ? Puisqu'une clé ne peut apparaître qu'une fois, seul le dernier nom rencontré est conservé.
````

```{raw} latex
\fi
```

(ex7.5)=
```{admonition} Exercice 7.5 : Bulletin de notes ★★★
On représente les notes d'une classe par un dictionnaire associant à chaque prénom la liste de ses notes (comme dans la section « Des valeurs plus riches »).

1. Écrivez une fonction `moyennes(notes)` qui retourne un dictionnaire associant à chaque prénom sa moyenne.
2. Écrivez une fonction `admis(notes)` qui retourne la liste triée par ordre alphabétique des prénoms dont la moyenne est supérieure ou égale à 10.
3. Écrivez une fonction `ajoute_note(notes, prenom, note)` qui ajoute une note à un étudiant, en créant son entrée s'il n'existe pas encore.
```

<div id="pad_7_5" class="pad"></div>
<script>
    Pythonpad('pad_7_5', {'id': 'aude_7.5', 'title': 'Testez votre code ici', 'src': "notes = {\"Aude\": [12, 15, 17], \"Ali\": [9, 8], \"Chloé\": [16, 13, 18, 11]}\n\ndef moyennes(notes):\n    # Complétez ce code\n    pass\n\nprint(moyennes(notes))\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
def moyennes(notes):
    resultat = {}
    for prenom, liste_notes in notes.items():
        resultat[prenom] = sum(liste_notes) / len(liste_notes)
    return resultat

def admis(notes):
    liste_admis = []
    for prenom, moyenne in moyennes(notes).items():
        if moyenne >= 10:
            liste_admis.append(prenom)
    return sorted(liste_admis)

def ajoute_note(notes, prenom, note):
    if prenom in notes:
        notes[prenom].append(note)
    else:
        notes[prenom] = [note]

notes = {"Aude": [12, 15, 17], "Ali": [9, 8], "Chloé": [16, 13, 18, 11]}
print(moyennes(notes))
print(admis(notes))
ajoute_note(notes, "Ali", 20)
ajoute_note(notes, "Margot", 14)
print(notes)
print(admis(notes))
```

Remarquez que `ajoute_note` ne retourne rien : elle **modifie** le dictionnaire reçu en argument (comme pour les listes, le dictionnaire n'est pas copié lors de l'appel de la fonction).
````

```{raw} latex
\fi
```

(ex7.6)=
```{admonition} Exercice 7.6 : Lettres communes ★
Écrivez une fonction `lettres_communes(mot1, mot2)` qui retourne la liste **triée** des lettres présentes à la fois dans `mot1` et dans `mot2`.
```

<div id="pad_7_6" class="pad"></div>
<script>
    Pythonpad('pad_7_6', {'id': 'aude_7.6', 'title': 'Testez votre code ici', 'src': "def lettres_communes(mot1, mot2):\n    # Complétez ce code\n    pass\n\nprint(lettres_communes(\"python\", \"typographie\"))  # doit afficher ['h', 'o', 'p', 't', 'y']\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
def lettres_communes(mot1, mot2):
    return sorted(set(mot1) & set(mot2))

print(lettres_communes("python", "typographie"))
```

`set` appliqué à une chaîne donne l'ensemble de ses caractères, et `sorted` accepte n'importe quelle collection et retourne toujours une liste.
````

```{raw} latex
\fi
```

## Bilan du chapitre

```{admonition} À retenir
:class: important

* Création : `d = {"cle1": valeur1, "cle2": valeur2}` ou `d = {}`.
* Lecture : `d[cle]` (erreur `KeyError` si la clé n'existe pas) ou `d.get(cle, valeur_par_defaut)`.
* Écriture : `d[cle] = valeur` (crée ou remplace) ; suppression : `del d[cle]`.
* `cle in d` teste la présence d'une **clé**.
* Parcours : `for cle in d.keys()`, `for valeur in d.values()`, `for cle, valeur in d.items()`.
* Compter : `d[x] = d.get(x, 0) + 1`.
* _Tuple_ : `(3, 7)`, non modifiable ; déballage `x, y = point`. _Set_ : `set(liste)` pour les valeurs distinctes.
```

Faites le point : êtes-vous capable de…

- créer un dictionnaire, lire et modifier une valeur à partir de sa clé ?
- éviter une `KeyError` avec `in` ou `get` ?
- parcourir un dictionnaire en récupérant à la fois les clés et les valeurs ?
- compter des occurrences avec un dictionnaire ?
- déballer un _tuple_ et obtenir les valeurs distinctes d'une liste ?
- choisir entre une liste, un dictionnaire, un _tuple_ et un _set_ ?
