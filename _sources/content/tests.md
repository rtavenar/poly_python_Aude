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

(ch:tests)=
# Déboguer et tester son code

```{admonition} Objectifs du chapitre
:class: note

À la fin de ce chapitre, vous saurez :

* lire un message d'erreur et reconnaître les types d'erreurs les plus courants ;
* adopter une démarche méthodique pour trouver un _bug_ ;
* écrire des tests unitaires simples, avec `print` ou avec `assert` ;

**Prérequis :** chapitres 1 à 5. **Durée indicative :** 1h.
```

```{admonition} Pour info
:class: seealso

Il existe en Python des outils dédiés au test de programmes (comme `pytest` ou `unittest`).
Ce chapitre ne traite pas de ces outils, mais de l'intérêt des tests en général et de bonnes habitudes à prendre dès le début.
```

Dans ce document, nous avons jusqu'à présent supposé que tout se passait bien : que votre code ne produisait jamais d'erreur et ne contenait jamais de _bug_.
Quel que soit votre niveau en Python, ces deux hypothèses sont peu réalistes !
Nous allons donc voir comment vérifier si votre code fait bien ce que l'on attend de lui, et comment comprendre son comportement lorsque ce n'est pas le cas.

On distingue deux situations :

* le programme **s'arrête avec un message d'erreur** : c'est la situation la plus simple, car Python vous indique où et pourquoi ;
* le programme **s'exécute sans erreur mais donne un résultat faux** : c'est un _bug_ « silencieux », plus difficile à trouver, et c'est là que les tests sont indispensables.

## Les erreurs en Python

### Lire un message d'erreur

Étudions ce qu'il se passe lors de l'exécution du code suivant :

```{code-cell}
:tags: ["raises-exception"]
x = "12"
y = x + 2
```

```{figure} ../img/fig_erreur.*
:width: 95%

Rappel du chapitre 1 : anatomie d'un message d'erreur.
```

Ce type de message ne doit pas vous effrayer, il est là pour vous aider.
Il vous fournit de précieuses informations :

1. l'erreur se produit à la ligne 2 du code ;
2. le problème est une `TypeError` : Python ne peut concaténer (`concatenate`) une chaîne (`str`) qu'avec une autre chaîne, et non avec un entier (`int`).

Reste à comprendre pourquoi.
Dans la ligne 2 (`y = x + 2`), deux opérations sont effectuées : l'opération `+` entre `x` et `2`, puis l'affectation du résultat à `y`.
Nous avons vu que Python sait effectuer l'opération `+` avec des opérandes de types variés (nombre + nombre, liste + liste, chaîne + chaîne…).
Intéressons-nous donc au type des opérandes : `x`, définie à la ligne 1, est une chaîne de caractères, tandis que `2` est un entier.
Or Python ne définit pas d'addition entre une chaîne et un entier.
Plus précisément, Python nous dit : « si je pouvais convertir l'entier en chaîne de caractères à la volée, je pourrais faire l'opération `+`, qui serait alors une concaténation, mais je ne me permets pas de le faire sans que vous l'ayez écrit explicitement ».

Maintenant que nous avons compris le sens de ce _bug_, il nous reste à le corriger.
Si nous souhaitons faire la somme du nombre 12 (stocké sous forme de chaîne de caractères dans la variable `x`) et de la valeur 2, nous écrivons :

```{code-cell}
x = "12"
y = int(x) + 2
print(y)
```

Lorsque l'erreur se produit à l'intérieur d'une fonction, le message d'erreur liste toute la **pile d'appels** : la ligne du programme principal qui a appelé la fonction, puis la ligne de la fonction où l'erreur s'est produite.
C'est généralement la **dernière** ligne de code mentionnée qui est la plus intéressante.

### Les erreurs les plus courantes

Voici un récapitulatif des erreurs rencontrées dans ce document :

| Type d'erreur | Signification | Exemple typique |
|---|---|---|
| `SyntaxError` | le code ne respecte pas la « grammaire » de Python | `:` ou parenthèse oubliés, `=` au lieu de `==` |
| `IndentationError` | décalages incorrects | bloc non indenté après un `if` |
| `NameError` | nom (variable, fonction) inconnu | faute de frappe, variable utilisée avant d'être définie, module non importé |
| `TypeError` | opération impossible pour ce type de données | `"12" + 2`, mauvais nombre d'arguments dans un appel |
| `ValueError` | bon type mais valeur incorrecte | `int("douze")`, `liste.remove(x)` si `x` est absent |
| `IndexError` | indice hors de la liste | `liste[len(liste)]` |
| `KeyError` | clé absente d'un dictionnaire | `d["cle_inexistante"]` |
| `AttributeError` | attribut ou méthode inexistant pour cet objet | `liste.lower()`, `None.append(...)` |
| `ZeroDivisionError` | division par zéro | `moyenne` d'une liste vide |
| `FileNotFoundError` | fichier introuvable | mauvais nom ou mauvais dossier |

```{admonition} Testez-vous
:class: hint

Quel type d'erreur produit chacune de ces lignes ?

1. `print(len(5))`
2. `[1, 2, 3][3]`
3. `prnt("bonjour")`
4. `float("3,5")`
5. `{"a": 1}["b"]`
6. `"abc".append("d")`
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

1. `TypeError` : un entier n'a pas de longueur ;
2. `IndexError` : les indices valides vont de 0 à 2 ;
3. `NameError` : faute de frappe dans `print` ;
4. `ValueError` : la virgule n'est pas acceptée (il faut un point) ;
5. `KeyError` ;
6. `AttributeError` : les chaînes n'ont pas de méthode `append`.
```

```{raw} latex
\fi
```

## Trouver un _bug_ : une démarche méthodique

Lorsqu'un programme ne fait pas ce qu'il devrait, il est tentant de modifier le code un peu au hasard jusqu'à ce que « ça marche ».
C'est rarement efficace ! Voici une démarche plus fiable.

1. **Reproduire le problème** sur un exemple aussi petit que possible, dont vous connaissez le résultat attendu.
2. **Lire le message d'erreur** s'il y en a un, en commençant par la dernière ligne.
3. **Observer** ce que fait réellement le programme : affichez les valeurs des variables avec `print` à des endroits stratégiques (au début d'une fonction, à chaque tour de boucle…), ou exécutez le code pas à pas avec Python Tutor ou le débogueur de Thonny.
4. **Comparer** avec ce que vous attendiez : à quel moment la valeur d'une variable s'écarte-t-elle de ce que vous aviez prévu ? Le _bug_ se trouve juste avant.
5. **Corriger**, puis **re-tester** tous vos exemples (une correction peut en casser une autre !).

### Exemple guidé

La fonction suivante est censée calculer la moyenne des valeurs positives d'une liste.
Elle s'exécute sans erreur… mais le résultat est faux : la moyenne des valeurs positives de `[4, -2, 6]` devrait valoir 5.

```{code-cell}
def moyenne_positifs(liste):
    somme = 0
    nb = 0
    for x in liste:
        if x > 0:
            somme += x
        nb += 1
    return somme / nb

print(moyenne_positifs([4, -2, 6]))
```

Ajoutons un affichage dans la boucle pour observer l'évolution des variables :

```{code-cell}
def moyenne_positifs(liste):
    somme = 0
    nb = 0
    for x in liste:
        if x > 0:
            somme += x
        nb += 1
        print(f"x = {x}, somme = {somme}, nb = {nb}")   # affichage de débogage
    return somme / nb

print(moyenne_positifs([4, -2, 6]))
```

L'affichage montre que `nb` est incrémenté même lorsque `x = -2` : l'instruction `nb += 1` est mal indentée, elle devrait se trouver **dans** le bloc du `if`.
Une fois le _bug_ corrigé, on n'oublie pas de retirer l'affichage de débogage :

```{code-cell}
def moyenne_positifs(liste):
    somme = 0
    nb = 0
    for x in liste:
        if x > 0:
            somme += x
            nb += 1
    return somme / nb

print(moyenne_positifs([4, -2, 6]))
```

Remarquez au passage que cette fonction produira une `ZeroDivisionError` si la liste ne contient aucune valeur positive : selon l'usage prévu, il faudrait peut-être traiter ce cas à part (en retournant `None`, par exemple).

## Les tests unitaires

### Pourquoi tester ?

Pour avoir confiance dans le code que vous écrivez, il faut l'avoir testé sur un ensemble d'exemples qui reflète l'ensemble des situations auxquelles votre programme pourra être confronté.
Or, cela représente vite un grand nombre de cas dès que le programme devient un peu complexe.
Il est donc recommandé de **découper son code en fonctions** de tailles raisonnables, qui puissent être testées indépendamment les unes des autres.
Les tests associés à chacune de ces fonctions sont appelés **tests unitaires**.

Mettre en place de tels tests présente plusieurs avantages :

* vous détectez rapidement un éventuel _bug_, ce qui fait gagner beaucoup de temps ;
* lorsque vous modifiez votre code plus tard (pour le corriger ou lui ajouter une fonctionnalité), vous pouvez relancer les tests pour vous assurer que vous n'avez rien cassé dans les cas qui fonctionnaient déjà.

### Choisir ses tests

Prenons un exemple concret.
Supposons que l'on souhaite écrire une fonction `bissextile` capable de dire si une année est bissextile.
En se renseignant sur [le sujet](https://fr.wikipedia.org/wiki/Ann%C3%A9e_bissextile), on apprend qu'une année est bissextile :

* si elle est divisible par 4 et non divisible par 100, ou
* si elle est divisible par 400.

On en déduit un ensemble de tests couvrant les différents cas de figure :

```python
print(bissextile(2004))  # True car divisible par 4 et non par 100
print(bissextile(1900))  # False car divisible par 100 et non par 400
print(bissextile(2000))  # True car divisible par 400
print(bissextile(1999))  # False car non divisible par 4
```

```{admonition} À retenir : comment choisir ses tests ?
:class: important

* Un test par **cas de figure** distinct de l'énoncé (ici, les 4 situations possibles).
* Des **cas limites** : liste vide, liste à un seul élément, valeur nulle, valeurs égales, première et dernière valeur d'un intervalle…
* Pour chaque test, **le résultat attendu doit être connu à l'avance** (calculé à la main, ou trouvé dans l'énoncé).
```

### Tester automatiquement avec `assert`

Avec des `print`, il faut vérifier « à l'œil » que chaque résultat affiché correspond au résultat attendu, ce qui devient fastidieux quand les tests sont nombreux.
L'instruction `assert` permet d'automatiser cette vérification : `assert condition` ne fait rien si la condition est vraie, et provoque une erreur (`AssertionError`) si elle est fausse.

```{code-cell}
:tags: [raises-exception]
def bissextile(annee):
    return annee % 4 == 0   # version incomplète, volontairement fausse

assert bissextile(2004) == True
assert bissextile(1999) == False
assert bissextile(2000) == True
assert bissextile(1900) == False   # ce test échoue
print("Tous les tests sont passés !")
```

Le message d'erreur indique précisément quel test a échoué.
On peut regrouper les tests d'une fonction dans une fonction de test, que l'on relance après chaque modification :

```{code-cell}
def bissextile(annee):
    if annee % 4 == 0 and annee % 100 != 0:
        return True
    elif annee % 400 == 0:
        return True
    else:
        return False

def test_bissextile():
    assert bissextile(2004) == True    # divisible par 4 et non par 100
    assert bissextile(1900) == False   # divisible par 100 et non par 400
    assert bissextile(2000) == True    # divisible par 400
    assert bissextile(1999) == False   # non divisible par 4
    print("test_bissextile : OK")

test_bissextile()
```

```{admonition} Attention avec les nombres à virgule
:class: warning

À cause des erreurs d'arrondi, `assert 0.1 + 0.2 == 0.3` échoue !
Pour tester des résultats à virgule, on vérifie plutôt que l'écart est très petit : `assert abs(resultat - attendu) < 1e-9`.
```

## Exercices

(ex8.1)=
```{admonition} Exercice 8.1 : Trouvez les bugs ★★
Chacune des fonctions suivantes contient (au moins) un _bug_.
Pour chacune, écrivez d'abord un ou plusieurs tests qui mettent le _bug_ en évidence, puis corrigez la fonction.

    # Doit retourner le plus grand élément d'une liste non vide
    def maximum(liste):
        m = 0
        for x in liste:
            if x > m:
                m = x
        return m

    # Doit retourner le nombre de voyelles d'un mot
    def nb_voyelles(mot):
        n = 0
        for lettre in mot:
            if lettre in "aeiouy":
                n += 1
            return n

    # Doit retourner la liste des éléments pairs de la liste
    def pairs(liste):
        resultat = []
        for i in range(len(liste)):
            if i % 2 == 0:
                resultat.append(liste[i])
        return resultat
```

<div id="pad_8_1" class="pad"></div>
<script>
    Pythonpad('pad_8_1', {'id': 'aude_8.1', 'title': 'Testez votre code ici', 'src': "def maximum(liste):\n    m = 0\n    for x in liste:\n        if x > m:\n            m = x\n    return m\n\ndef nb_voyelles(mot):\n    n = 0\n    for lettre in mot:\n        if lettre in \"aeiouy\":\n            n += 1\n        return n\n\ndef pairs(liste):\n    resultat = []\n    for i in range(len(liste)):\n        if i % 2 == 0:\n            resultat.append(liste[i])\n    return resultat\n\n# Écrivez vos tests ici, par exemple :\nassert maximum([1, 5, 3]) == 5\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

* `maximum` : que se passe-t-il si tous les éléments sont négatifs ?
* `nb_voyelles` : regardez bien l'indentation du `return`. Combien de tours de boucle sont effectués ?
* `pairs` : la fonction teste-t-elle la parité des éléments ou celle d'autre chose ?
```

````{admonition} Solution
:class: tip, dropdown

```python
# Bug 1 : m est initialisé à 0, donc le résultat est faux si tous les éléments sont négatifs.
# Test qui révèle le bug : assert maximum([-3, -1, -7]) == -1
def maximum(liste):
    m = liste[0]   # on initialise avec le premier élément
    for x in liste:
        if x > m:
            m = x
    return m

# Bug 2 : le return est dans la boucle, la fonction s'arrête dès la première lettre.
# Test qui révèle le bug : assert nb_voyelles("bonjour") == 3
def nb_voyelles(mot):
    n = 0
    for lettre in mot:
        if lettre in "aeiouy":
            n += 1
    return n

# Bug 3 : on teste la parité de l'indice i et non celle de l'élément liste[i].
# Test qui révèle le bug : assert pairs([1, 2, 3, 4]) == [2, 4]
def pairs(liste):
    resultat = []
    for elem in liste:
        if elem % 2 == 0:
            resultat.append(elem)
    return resultat

assert maximum([1, 5, 3]) == 5
assert maximum([-3, -1, -7]) == -1
assert nb_voyelles("bonjour") == 3
assert nb_voyelles("") == 0
assert pairs([1, 2, 3, 4]) == [2, 4]
assert pairs([]) == []
print("Tous les tests sont passés !")
```

Remarquez que chacun de ces _bugs_ passait inaperçu sur certains exemples (par exemple `maximum([1, 5, 3])` donnait bien 5) : d'où l'importance de choisir des tests variés, en pensant aux cas particuliers.
````

```{raw} latex
\fi
```

(ex8.2)=
````{admonition} Exercice 8.2 : Bissextile en une ligne ★★
Proposez une réécriture de la fonction `bissextile` qui tienne en une ligne de la forme :

```python
def bissextile(annee):
    return CONDITION_COMPLEXE
```

où `CONDITION_COMPLEXE` est un booléen calculé à partir de la valeur de `annee`.
Assurez-vous que cette nouvelle fonction passe bien les tests énoncés plus haut.
````

<div id="pad_8_2" class="pad"></div>
<script>
    Pythonpad('pad_8_2', {'id': 'aude_8.2', 'title': 'Testez votre code ici', 'src': "def bissextile(annee):\n    return ...  # Complétez ce code\n\nassert bissextile(2004) == True\nassert bissextile(1900) == False\nassert bissextile(2000) == True\nassert bissextile(1999) == False\nprint(\"Tous les tests sont passés !\")\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
def bissextile(annee):
    return (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0)

assert bissextile(2004) == True
assert bissextile(1900) == False
assert bissextile(2000) == True
assert bissextile(1999) == False
print("Tous les tests sont passés !")
```

C'est exactement l'intérêt des tests : on peut réécrire (on dit **refactoriser**) une fonction en toute confiance, puisque les tests nous assurent que son comportement n'a pas changé.
````

```{raw} latex
\fi
```

## Bilan du chapitre

```{admonition} À retenir
:class: important

* Un message d'erreur se lit en partant de la fin : type d'erreur, explication, puis ligne en cause.
* Pour trouver un _bug_ : reproduire sur un petit exemple, observer (`print`, Python Tutor, débogueur), comparer avec l'attendu, corriger, re-tester.
* Tester chaque fonction sur plusieurs cas, y compris les cas limites ; `assert condition` vérifie automatiquement un résultat.
```

Faites le point : êtes-vous capable de…

- associer un type d'erreur (`TypeError`, `IndexError`…) à sa cause probable ?
- utiliser des `print` pour localiser un _bug_ silencieux ?
- choisir un jeu de tests pertinent pour une fonction, avec des cas limites ?
- écrire une fonction de test utilisant `assert` ?
