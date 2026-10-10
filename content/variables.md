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

(ch:variables)=
# Variables, types et opérations

```{admonition} Objectifs du chapitre
:class: note

À la fin de ce chapitre, vous saurez :

* afficher du texte et des résultats de calcul avec `print` ;
* créer des variables, leur donner des valeurs et connaître leur type ;
* utiliser les opérateurs arithmétiques (`+`, `-`, `*`, `/`, `//`, `%`, `**`) ;
* convertir une valeur d'un type à un autre (`int`, `float`, `str`) ;
* lire un message d'erreur Python.

**Durée indicative :** 1h30.
```

## Un tout premier programme

Commençons par le plus simple des programmes : afficher un message à l'écran.
On utilise pour cela la **fonction** `print` :

```{code-cell}
print("Bonjour !")
```

Le texte à afficher est placé **entre guillemets** (on parle de _chaîne de caractères_) et **entre parenthèses** après le mot `print`.
On peut aussi demander à Python d'afficher le résultat d'un calcul :

```{code-cell}
print(12 * 5)
```

ou encore afficher plusieurs choses à la suite, séparées par des virgules (Python insère alors un espace entre elles) :

```{code-cell}
print("12 fois 5 font", 12 * 5)
```

Un programme est une **suite d'instructions** exécutées les unes après les autres, de haut en bas :

```{code-cell}
print("Première ligne")
print("Deuxième ligne")
print("Troisième ligne")
```

Enfin, tout ce qui suit un symbole `#` sur une ligne est un **commentaire** : Python l'ignore complètement.
Les commentaires servent à expliquer le code aux humains qui le lisent (y compris vous-même dans trois semaines !).

```{code-cell}
# Ceci est un commentaire : il n'est pas exécuté
print("Le commentaire n'a rien affiché")  # on peut aussi commenter en fin de ligne
```

```{admonition} Testez-vous
:class: hint

Qu'affiche le programme suivant ?

    print("3 + 4")
    print(3 + 4)
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

Il affiche :

    3 + 4
    7

Dans la première ligne, `"3 + 4"` est entre guillemets : c'est un texte, que Python affiche tel quel.
Dans la seconde, `3 + 4` est un calcul que Python effectue avant d'afficher le résultat.
```

```{raw} latex
\fi
```

## Les variables

### Qu'est-ce qu'une variable ?

Dès qu'un programme fait plus que quelques calculs, on a besoin de **mémoriser des valeurs** pour les réutiliser plus tard.
En Python, les données sont stockées dans des **variables**.
Une variable est une association entre un **nom** (choisi par vous) et une **valeur**, qui peut changer au cours de l'exécution du programme.

On peut se représenter une variable comme une **étiquette** portant un nom, accrochée à une boîte qui contient une valeur :

```{figure} ../img/fig_variables.*
:width: 85%

Quatre variables et leurs valeurs. Chaque valeur a un **type**.
```

Pour créer une variable, on utilise le signe `=`, appelé **opérateur d'affectation** :

```{code-cell}
age = 19
taille = 1.72
prenom = "Aude"
inscrite = True
```

Ces instructions n'affichent rien : elles se contentent de ranger des valeurs en mémoire.
On peut ensuite utiliser les variables en écrivant simplement leur nom :

```{code-cell}
print(prenom)
print(age + 1)
print(prenom, "mesure", taille, "m")
```

```{admonition} À retenir
:class: important

Le signe `=` en Python ne signifie **pas** « est égal à » comme en mathématiques, mais « **prend la valeur** ».
L'instruction `age = 19` se lit : « la variable `age` prend la valeur 19 ».
On met toujours **le nom de la variable à gauche** et **la valeur à droite**.
```

### Les types de base

Chaque valeur a un **type**, qui détermine ce que l'on peut faire avec elle.
Les types de base en Python sont les suivants :

| Type | Signification | Exemples |
|---|---|---|
| `int` | nombre entier (_integer_) | `12`, `-3`, `0` |
| `float` | nombre à virgule (_floating point number_) | `1.72`, `-0.5`, `12.` |
| `str` | chaîne de caractères (_string_), c'est-à-dire du texte | `"Aude"`, `'abc'`, `"12"` |
| `bool` | booléen : vrai ou faux | `True`, `False` |
| `complex` | nombre complexe (peu utilisé dans ce document) | `1 + 2j` |

Il existe de plus une valeur spéciale, `None`, qui signifie « pas de valeur » ou « valeur manquante » (son type est `NoneType`).

```{admonition} Erreur fréquente
:class: warning

* En Python, la virgule des nombres décimaux s'écrit avec un **point** : on écrit `1.72` et non `1,72`.
* Les chaînes de caractères peuvent être délimitées par des guillemets doubles (`"abc"`) ou simples (`'abc'`) : les deux sont équivalents, mais il faut utiliser le même au début et à la fin.
* `True` et `False` prennent une majuscule.
```

Pour connaître le type d'une valeur ou d'une variable, on utilise la fonction `type` :

```{code-cell}
print(type(age))
print(type(taille))
print(type(prenom))
print(type(inscrite))
```

En Python, on ne déclare pas le type d'une variable : il est déduit de la valeur qu'on y range.
Et si l'on range une valeur d'un autre type dans la même variable, son type change (on dit que Python est **typé dynamiquement**) :

```{code-cell}
v = 12        # v est de type entier
print(type(v))
v = 12.       # v change de type : c'est désormais un nombre à virgule
print(type(v))
```

```{admonition} Testez-vous
:class: hint

Quel est le type de chacune des valeurs suivantes ? `42`, `"42"`, `42.0`, `"vrai"`, `False`.
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

* `42` : `int` ;
* `"42"` : `str` (il y a des guillemets, c'est donc du texte, même s'il ne contient que des chiffres !) ;
* `42.0` : `float` ;
* `"vrai"` : `str` ;
* `False` : `bool`.

Vous pouvez vérifier chacune de ces réponses avec la fonction `type`.
```

```{raw} latex
\fi
```

### Choisir un nom de variable

Les noms de variables doivent respecter quelques règles :

* ils doivent commencer par une lettre (minuscule ou majuscule) ou par le symbole `_` ;
* ils ne doivent contenir que des lettres, des chiffres et des symboles `_` (pas d'espace, pas de tiret `-`, pas d'apostrophe) ;
* ils ne doivent pas être un **mot réservé** du langage Python, dont voici la liste :

```
and del for is raise assert elif from lambda return break else global
not try nonlocal True False class except if or while continue import
pass yield None def finally in as with
```

* enfin, il est vivement conseillé de ne pas utiliser le nom d'une fonction existante de Python (comme `print`, `type`, `list`, `sum`…) : vous apprendrez ces noms au fur et à mesure.

Les noms de variables sont **sensibles à la casse** : `mavariable` et `maVariable` sont deux variables différentes.

```{code-cell}
mavariable = 12
maVariable = 15
print(mavariable)
print(maVariable)
```

```{admonition} Bonne pratique
:class: tip

Choisissez des noms **explicites** : `prix_total` est bien plus clair que `pt` ou `x`.
Un programme est écrit une fois mais relu de nombreuses fois !
En Python, l'usage est d'écrire les noms de variables en minuscules, avec des `_` pour séparer les mots (`nombre_etudiants`).
Les accents sont autorisés mais il est d'usage de les éviter.
```

```{admonition} Testez-vous
:class: hint

Parmi les noms suivants, lesquels sont des noms de variables valides ?
`note1`, `1ere_note`, `note-finale`, `note_finale`, `_temp`, `for`, `Note`.
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

* `note1` : valide ;
* `1ere_note` : **invalide** (commence par un chiffre) ;
* `note-finale` : **invalide** (le `-` est interprété comme une soustraction) ;
* `note_finale` : valide ;
* `_temp` : valide ;
* `for` : **invalide** (mot réservé) ;
* `Note` : valide (mais c'est une autre variable que `note`).
```

```{raw} latex
\fi
```

## L'affectation en détail

La règle de l'affectation est la suivante : « **calculer** la valeur de ce qui est à droite du `=`, puis **ranger** le résultat dans la variable de gauche ».
Il est donc tout à fait valide d'écrire :

```{code-cell}
x = 5
x = x + 2
print(x)
```

Mathématiquement, `x = x + 2` n'a aucun sens.
Mais en Python, cette instruction se lit : « `x` prend la valeur (ancienne valeur de `x`) + 2 ».

```{figure} ../img/fig_affectation.*
:width: 85%

Les deux temps de l'affectation `x = x + 2` : d'abord le calcul à droite, ensuite le rangement à gauche (l'ancienne valeur est perdue).
```

Le même principe s'applique pour des expressions plus complexes :

```{code-cell}
x = 2
x = 3.9 * x * (1 - x)
print(x)
```

Pour exécuter la deuxième instruction, Python commence par évaluer `3.9 * x * (1 - x)` avec la valeur courante de `x` (2), obtient `-7.8`, puis range ce résultat dans `x`.

Comme les instructions sont exécutées dans l'ordre, la valeur d'une variable à un instant donné dépend de tout ce qui a été exécuté avant :

```{code-cell}
a = 3
b = a + 1
a = 10
print(a, b)
```

Remarquez que modifier `a` à la ligne 3 ne modifie pas `b` : au moment de la ligne 2, Python a calculé `a + 1` (qui valait 4) et a rangé **le résultat** dans `b`.

*[Voir ce code s'exécuter pas à pas dans Python Tutor](https://pythontutor.com/visualize.html#code=a%20%3D%203%0Ab%20%3D%20a%20%2B%201%0Aa%20%3D%2010%0Aprint%28a%2C%20b%29%0A&cumulative=false&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D&textReferences=false)*

```{admonition} Testez-vous
:class: hint

Que contiennent les variables `a` et `b` à la fin de ce programme ?

    a = 5
    b = 2
    a = b
    b = a
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

`a` et `b` valent toutes les deux 2.
À la ligne 3, `a` prend la valeur de `b`, soit 2 (et la valeur 5 est perdue).
À la ligne 4, `b` prend la valeur de `a`, qui vaut maintenant 2.
Ce programme n'échange donc **pas** les valeurs de `a` et `b` (c'est l'objet de l'exercice 1.5).
```

```{raw} latex
\fi
```

## Les opérations sur les nombres

### Les opérateurs arithmétiques

Voici les opérateurs disponibles pour les nombres (`int` et `float`) :

| Opérateur | Opération | Exemple | Résultat |
|:---:|:---:|:---:|:---:|
| `+` | Addition | `7 + 2` | `9` |
| `-` | Soustraction | `7 - 2` | `5` |
| `*` | Multiplication | `7 * 2` | `14` |
| `/` | Division | `7 / 2` | `3.5` |
| `**` | Puissance | `7 ** 2` | `49` |
| `//` | Division entière (quotient) | `7 // 2` | `3` |
| `%` | Modulo (reste de la division entière) | `7 % 2` | `1` |

Les deux derniers opérateurs méritent qu'on s'y arrête : ce sont ceux de la division que vous avez apprise à l'école primaire.
Si l'on partage 17 bonbons entre 5 enfants, chaque enfant en reçoit 3 et il en reste 2 :

```{code-cell}
print(17 // 5)  # quotient : nombre de bonbons par enfant
print(17 % 5)   # reste : nombre de bonbons restants
```

```{admonition} À retenir
:class: important

L'opérateur `%` (modulo) est très utile en pratique :

* `n % 2` vaut `0` si `n` est pair et `1` si `n` est impair ;
* plus généralement, `n % k == 0` signifie « `n` est divisible par `k` » ;
* `n % 10` donne le dernier chiffre d'un entier positif `n`.
```

Notez que la division `/` donne toujours un `float`, même si le résultat « tombe juste » :

```{code-cell}
print(6 / 3)
print(2 / 3)
```

De manière générale, lorsqu'une opération mêle un `int` et un `float`, le résultat est un `float`.

````{admonition} Les nombres à virgule sont approximatifs
:class: seealso

Les ordinateurs stockent les nombres à virgule avec une précision limitée, ce qui donne parfois des résultats surprenants.
Par exemple, `print(0.1 + 0.2)` affiche `0.30000000000000004`.
Ce n'est pas un bug de Python : la plupart des langages de programmation se comportent de la même façon.
Retenez simplement qu'il faut éviter de tester l'égalité exacte entre deux nombres à virgule, et utiliser l'affichage avec un nombre fixé de décimales (voir plus bas) pour présenter les résultats.
````

### Priorité des opérateurs

Lorsqu'une expression contient plusieurs opérateurs, Python applique les mêmes règles de priorité qu'en mathématiques (de la priorité la plus forte à la plus faible) :

1. parenthèses ;
2. puissance `**` ;
3. multiplication, divisions et modulo (`*`, `/`, `//`, `%`) ;
4. addition et soustraction ;
5. à priorité égale, de gauche à droite.

```{code-cell}
print(2 + 3 * 4)
print((2 + 3) * 4)
print(2 * 3 ** 2)
```

En cas de doute, ajoutez des parenthèses : cela ne coûte rien et rend le code plus lisible.

### Les opérateurs raccourcis

Il est très fréquent de modifier une variable à partir de sa propre valeur (par exemple pour compter quelque chose).
Pour cela, il existe des raccourcis d'écriture : `x += 2` est équivalent à `x = x + 2`.

```{code-cell}
compteur = 0
compteur += 1   # équivaut à compteur = compteur + 1
compteur += 1
print(compteur)
```

Il en va de même pour `-=`, `*=`, `/=`, _etc._
Ce n'est qu'un raccourci : si vous ne vous sentez pas à l'aise avec, vous pouvez toujours écrire `x = x + 2`.

```{admonition} Testez-vous
:class: hint

Que valent les expressions suivantes ? `10 // 3`, `10 % 3`, `10 / 4`, `2 ** 3 + 1`, `15 % 5`.
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

* `10 // 3` vaut `3` (10 = 3 × 3 + 1) ;
* `10 % 3` vaut `1` ;
* `10 / 4` vaut `2.5` ;
* `2 ** 3 + 1` vaut `9` (la puissance est prioritaire) ;
* `15 % 5` vaut `0` (15 est divisible par 5).
```

```{raw} latex
\fi
```

## Opérations sur les chaînes et conversions

### Concaténation

Certains opérateurs fonctionnent aussi avec les chaînes de caractères, avec un sens différent :
`+` met deux chaînes bout à bout (on dit qu'on les **concatène**) et `*` répète une chaîne.

```{code-cell}
prenom = "Aude"
print("Bonjour " + prenom + " !")
print("ha" * 3)
```

### Conversions de type

On ne peut pas additionner directement un texte et un nombre.
Il faut d'abord **convertir** l'un des deux dans le type de l'autre, à l'aide des fonctions `int`, `float` et `str` :

```{code-cell}
texte = "12"
nombre = int(texte)      # conversion de str vers int
print(nombre + 2)

age = 19
print("J'ai " + str(age) + " ans")  # conversion de int vers str

print(float("3.5") * 2)  # conversion de str vers float
print(int(3.99))         # int() tronque : on garde la partie entière
```

```{admonition} Testez-vous
:class: hint

Qu'affichent les instructions suivantes ?

    print("5" + "5")
    print(5 + 5)
    print("5" * 3)
    print(int("5") * 3)
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

    55
    10
    555
    15

Sur des chaînes, `+` concatène et `*` répète ; sur des nombres, ce sont l'addition et la multiplication habituelles.
```

```{raw} latex
\fi
```

### Afficher joliment : les f-strings

Construire un message avec des `+` et des `str()` devient vite pénible.
Python propose une écriture bien plus pratique, les **f-strings** : on place un `f` juste avant les guillemets et on écrit les noms de variables (ou des calculs) entre accolades `{}` dans le texte.

```{code-cell}
prenom = "Aude"
age = 19
print(f"{prenom} a {age} ans et aura {age + 1} ans l'an prochain.")
```

On peut aussi contrôler le nombre de décimales affichées avec `:.2f` (2 chiffres après la virgule) :

```{code-cell}
prix = 10 / 3
print(f"Prix : {prix} euros")
print(f"Prix : {prix:.2f} euros")
```

Vous rencontrerez aussi parfois une autre écriture, plus ancienne, qui utilise la méthode `format` : `"{} a {} ans".format(prenom, age)`.
Nous reviendrons sur ces deux façons de faire au {ref}`chapitre sur les chaînes de caractères <ch:chaines>`.

## Lire un message d'erreur

En programmant, vous ferez des erreurs : **c'est normal et cela arrive à tout le monde**, débutant·e ou expert·e.
Python vous aide en affichant un message d'erreur qu'il faut apprendre à lire.
Voici ce qui se passe si l'on essaie d'additionner un texte et un nombre :

```{code-cell}
:tags: [raises-exception]
x = "12"
y = x + 2
```

Ce message peut sembler effrayant, mais il contient des informations précieuses :

```{figure} ../img/fig_erreur.*
:width: 95%

Anatomie d'un message d'erreur (_traceback_) dans un script. La ligne la plus importante est la **dernière**.
```

1. **Où ?** Le message indique la ligne du programme où l'erreur s'est produite (ici la ligne 2, `y = x + 2`).
2. **Quel type d'erreur ?** Ici une `TypeError`, c'est-à-dire un problème de type de données.
3. **Quelle explication ?** « can only concatenate str (not "int") to str » : on ne peut concaténer (coller) une chaîne qu'avec une autre chaîne, pas avec un entier.

En effet, `x` contient le texte `"12"` (et non le nombre 12).
Pour corriger, il suffit de convertir `x` en entier :

```{code-cell}
x = "12"
y = int(x) + 2
print(y)
```

```{admonition} Erreurs fréquentes de ce chapitre
:class: warning

| Message d'erreur | Cause probable | Correction |
|---|---|---|
| `NameError: name 'prnom' is not defined` | faute de frappe dans un nom de variable, ou variable utilisée avant d'avoir été créée | vérifier l'orthographe (et les majuscules) |
| `SyntaxError: invalid syntax` | erreur de « grammaire » : parenthèse ou guillemet oublié, nom de variable invalide… | regarder la ligne indiquée **et la ligne précédente** |
| `SyntaxError: unterminated string literal` | guillemet fermant oublié | ajouter le guillemet |
| `TypeError: can only concatenate str (not "int") to str` | `+` entre un texte et un nombre | convertir avec `int()` ou `str()`, ou utiliser une f-string |
| `ValueError: invalid literal for int() with base 10: 'douze'` | conversion impossible | vérifier le contenu de la chaîne |
| `ZeroDivisionError: division by zero` | division par zéro | vérifier la valeur du diviseur |
```

Voici par exemple une `NameError`, due à une faute de frappe :

```{code-cell}
:tags: [raises-exception]
prenom = "Aude"
print(prnom)
```

````{admonition} Différences avec R et SAS
:class: seealso

* L'affectation s'écrit uniquement avec `=` (pas de `<-`).
* En R, `x <- 5` crée un vecteur de longueur 1 ; en Python, `5` est un simple nombre, et une suite de valeurs est une **liste** (chapitre 5) ou un tableau `numpy` (chapitre 10). Les opérations « vectorisées » auxquelles vous êtes habitué·e n'existent qu'avec `numpy` et `pandas`.
* La division `/` donne toujours un nombre à virgule ; la division entière s'écrit `//` (`%/%` en R) et le reste `%` (`%%` en R).
* Les valeurs logiques s'écrivent `True` et `False` (et non `TRUE` / `FALSE`), et la valeur manquante « générique » est `None` (avec `pandas`, ce sera `NaN`, l'équivalent de `NA` en R et de `.` en SAS).
* Dans un script, seul `print` affiche quelque chose : contrairement à la console R, une expression seule sur une ligne n'est pas affichée (sauf dans la console Python ou en dernière ligne d'une cellule de notebook).
````

## Exercices

(ex1.1)=
```{admonition} Exercice 1.1 : Conversion de températures ★
La température en degrés Fahrenheit $F$ s'obtient à partir de la température en degrés Celsius $C$ par la formule $F = \frac{9}{5} C + 32$.

Écrivez un programme qui, à partir d'une température en degrés Celsius stockée dans une variable `celsius`, calcule la température en degrés Fahrenheit, la stocke dans une variable `fahrenheit` et l'affiche sous la forme `20 °C = 68.0 °F`.
```

<div id="pad_1_1" class="pad"></div>
<script>
    Pythonpad('pad_1_1', {'id': 'aude_1.1', 'title': 'Testez votre code ici', 'src': "celsius = 20\n# Complétez ce code\n# Résultat attendu pour celsius = 20 : 20 °C = 68.0 °F\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

La traduction de la formule en Python est `9 / 5 * celsius + 32`.
Pour l'affichage, utilisez une f-string : `f"{celsius} °C = ..."`.
```

````{admonition} Solution
:class: tip, dropdown

```python
celsius = 20
fahrenheit = 9 / 5 * celsius + 32
print(f"{celsius} °C = {fahrenheit} °F")
```

Testez avec d'autres valeurs : -40 °C doit donner -40 °F, et 100 °C doit donner 212 °F.
````

```{raw} latex
\fi
```

(ex1.2)=
```{admonition} Exercice 1.2 : Prix TTC ★
Un article coûte `prix_ht` euros hors taxes. La TVA est de 20 %.
Écrivez un programme qui calcule et affiche le montant de la TVA et le prix toutes taxes comprises (TTC), avec deux chiffres après la virgule.
Pour `prix_ht = 49.99`, on doit obtenir :

    TVA : 10.00 euros
    Prix TTC : 59.99 euros
```

<div id="pad_1_2" class="pad"></div>
<script>
    Pythonpad('pad_1_2', {'id': 'aude_1.2', 'title': 'Testez votre code ici', 'src': "prix_ht = 49.99\ntaux_tva = 0.20\n# Complétez ce code\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

La TVA vaut `prix_ht * taux_tva` et le prix TTC est la somme du prix hors taxes et de la TVA.
Pour afficher deux décimales, utilisez `{variable:.2f}` dans une f-string.
```

````{admonition} Solution
:class: tip, dropdown

```python
prix_ht = 49.99
taux_tva = 0.20
tva = prix_ht * taux_tva
prix_ttc = prix_ht + tva
print(f"TVA : {tva:.2f} euros")
print(f"Prix TTC : {prix_ttc:.2f} euros")
```

Stocker le taux dans une variable (`taux_tva`) plutôt que d'écrire `0.20` directement dans le calcul rend le programme plus lisible et plus facile à modifier si le taux change.
````

```{raw} latex
\fi
```

(ex1.3)=
```{admonition} Exercice 1.3 : Heures, minutes, secondes ★★
Une durée est donnée en secondes dans une variable `duree` (par exemple `duree = 4000`).
Écrivez un programme qui affiche cette durée en heures, minutes et secondes.
Pour 4000 secondes, on doit obtenir : `4000 s = 1 h 6 min 40 s`.
```

<div id="pad_1_3" class="pad"></div>
<script>
    Pythonpad('pad_1_3', {'id': 'aude_1.3', 'title': 'Testez votre code ici', 'src': "duree = 4000\n# Complétez ce code\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Une heure dure 3600 secondes.
Le nombre d'heures est donc le quotient `duree // 3600`, et le **reste** `duree % 3600` est le nombre de secondes qui ne forment pas une heure complète.
Recommencez ensuite avec ce reste et 60 secondes par minute.
```

````{admonition} Solution
:class: tip, dropdown

```python
duree = 4000
heures = duree // 3600
reste = duree % 3600          # secondes restantes une fois les heures retirées
minutes = reste // 60
secondes = reste % 60
print(f"{duree} s = {heures} h {minutes} min {secondes} s")
```

Vérification : 1 × 3600 + 6 × 60 + 40 = 3600 + 360 + 40 = 4000. ✅
````

```{raw} latex
\fi
```

(ex1.4)=
```{admonition} Exercice 1.4 : Chiffres d'un nombre ★★
Soit `n` un nombre entier positif à trois chiffres (par exemple `n = 472`).
Écrivez un programme qui affiche séparément son chiffre des unités, son chiffre des dizaines et son chiffre des centaines, puis la somme de ses chiffres.
```

<div id="pad_1_4" class="pad"></div>
<script>
    Pythonpad('pad_1_4', {'id': 'aude_1.4', 'title': 'Testez votre code ici', 'src': "n = 472\n# Complétez ce code\n# Résultat attendu : unités 2, dizaines 7, centaines 4, somme 13\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

`n % 10` donne le chiffre des unités.
Que donne `n // 10` ? Et `(n // 10) % 10` ?
```

````{admonition} Solution
:class: tip, dropdown

```python
n = 472
unites = n % 10               # 2
dizaines = (n // 10) % 10     # 47 % 10 -> 7
centaines = n // 100          # 4
print("unités :", unites)
print("dizaines :", dizaines)
print("centaines :", centaines)
print("somme des chiffres :", unites + dizaines + centaines)
```
````

```{raw} latex
\fi
```

(ex1.5)=
```{admonition} Exercice 1.5 : Échanger deux variables ★★
On dispose de deux variables `a = 5` et `b = 8`.
Écrivez un programme qui **échange** leurs valeurs (à la fin, `a` doit valoir 8 et `b` doit valoir 5), sans écrire les nombres 5 et 8 ailleurs que dans les deux premières lignes.
Relisez la question « Testez-vous » de la section sur l'affectation : le piège y est décrit !
```

<div id="pad_1_5" class="pad"></div>
<script>
    Pythonpad('pad_1_5', {'id': 'aude_1.5', 'title': 'Testez votre code ici', 'src': "a = 5\nb = 8\n# Complétez ce code\nprint(a, b)  # doit afficher 8 5\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Pensez à la façon dont vous échangeriez le contenu de deux verres (un verre de jus d'orange et un verre de lait) : il vous faut un troisième verre !
```

````{admonition} Solution
:class: tip, dropdown

On utilise une troisième variable pour mettre de côté la valeur de `a` avant de l'écraser :

```python
a = 5
b = 8
temp = a    # on sauvegarde la valeur de a
a = b       # a prend la valeur de b (l'ancienne valeur de a est perdue, mais on l'a sauvegardée)
b = temp    # b prend l'ancienne valeur de a
print(a, b)
```

Python propose aussi une écriture plus compacte, que nous expliquerons au chapitre 7 :

```python
a = 5
b = 8
a, b = b, a
print(a, b)
```
````

```{raw} latex
\fi
```

(ex1.6)=
```{admonition} Exercice 1.6 : Ticket de caisse ★★★
Vous achetez `nb_croissants` croissants à 1,10 € pièce et `nb_baguettes` baguettes à 0,95 € pièce.
Vous payez avec un billet de 20 €.
Écrivez un programme qui affiche le montant total et la monnaie rendue, puis le nombre de pièces de 2 € qui seront rendues au maximum dans cette monnaie.

Pour 3 croissants et 2 baguettes, on doit obtenir :

    Total : 5.20 euros
    Monnaie : 14.80 euros
    Dont 7 pièce(s) de 2 euros
```

<div id="pad_1_6" class="pad"></div>
<script>
    Pythonpad('pad_1_6', {'id': 'aude_1.6', 'title': 'Testez votre code ici', 'src': "nb_croissants = 3\nnb_baguettes = 2\n# Complétez ce code\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Le nombre de pièces de 2 € est le quotient de la division entière de la monnaie par 2.
Le résultat est un `float` (par exemple `7.0`) : convertissez-le en entier avec `int()`.
```

````{admonition} Solution
:class: tip, dropdown

```python
nb_croissants = 3
nb_baguettes = 2
prix_croissant = 1.10
prix_baguette = 0.95

total = nb_croissants * prix_croissant + nb_baguettes * prix_baguette
monnaie = 20 - total
pieces_2_euros = int(monnaie // 2)

print(f"Total : {total:.2f} euros")
print(f"Monnaie : {monnaie:.2f} euros")
print(f"Dont {pieces_2_euros} pièce(s) de 2 euros")
```

Remarque : le calcul `int(monnaie // 2)` fonctionne car `monnaie // 2` vaut `7.0`, que `int` convertit en `7`.
````

```{raw} latex
\fi
```

## Bilan du chapitre

```{admonition} À retenir
:class: important

* `print(...)` affiche des valeurs ; le texte s'écrit entre guillemets.
* `variable = valeur` : on **calcule** ce qui est à droite puis on **range** le résultat dans la variable de gauche.
* Types de base : `int`, `float`, `str`, `bool` (et la valeur spéciale `None`). La fonction `type` donne le type d'une valeur.
* `//` donne le quotient de la division entière, `%` le reste ; `/` donne toujours un `float`.
* On convertit avec `int()`, `float()`, `str()`.
* `f"... {variable} ..."` permet d'insérer des valeurs dans un texte.
* Un message d'erreur se lit en commençant par **la dernière ligne**, puis en allant voir la ligne de code indiquée.
```

Faites le point : êtes-vous capable de…

- créer une variable, l'afficher et connaître son type ?
- prédire la valeur d'une variable après une suite d'affectations ?
- calculer un quotient et un reste avec `//` et `%` ?
- convertir un texte en nombre et inversement ?
- afficher un message contenant des valeurs de variables avec une f-string ?
- identifier, dans un message d'erreur, la ligne en cause et le type d'erreur ?

Si vous avez coché toutes les cases, passez au chapitre suivant. Sinon, relisez les sections correspondantes et refaites les exercices associés.
