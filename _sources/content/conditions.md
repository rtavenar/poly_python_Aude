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

(ch:conditions)=
# Les conditions

```{admonition} Objectifs du chapitre
:class: note

À la fin de ce chapitre, vous saurez :

* écrire des comparaisons (`<`, `==`, `!=`…) et les combiner (`and`, `or`, `not`) ;
* exécuter des instructions seulement si une condition est vraie (`if`) ;
* choisir entre plusieurs cas (`else`, `elif`) ;
* respecter les règles d’**indentation** de Python.

**Prérequis :** chapitre 1. **Durée indicative :** 1h30.
```

Jusqu'à présent, nos programmes exécutaient toutes leurs instructions, dans l'ordre, sans exception.
Mais souvent, on souhaite qu'un programme **réagisse différemment selon la situation** : afficher « admis » ou « ajourné » selon une note, appliquer une réduction seulement aux étudiants, _etc._
C'est le rôle des **structures conditionnelles**.

## Les booléens et les comparaisons

Une condition est une expression qui est soit vraie, soit fausse.
En Python, son résultat est un **booléen** (type `bool`) : `True` (vrai) ou `False` (faux).

```{code-cell}
note = 12
print(note >= 10)
print(note == 20)
```

Voici les opérateurs de comparaison à connaître :

| Opérateur | Signification | Exemple (avec `x = 5`) | Résultat |
|:---:|:---:|:---:|:---:|
| `<` | strictement plus petit que | `x < 5` | `False` |
| `>` | strictement plus grand que | `x > 0` | `True` |
| `<=` | plus petit ou égal à | `x <= 5` | `True` |
| `>=` | plus grand ou égal à | `x >= 6` | `False` |
| `==` | égal à | `x == 5` | `True` |
| `!=` | différent de | `x != 5` | `False` |
| `is` | test d'identité, pour comparer à `None` | `x is None` | `False` |
| `is not` | contraire de `is` | `x is not None` | `True` |
| `in` | présence d'une valeur dans une liste | `x in [1, 5, 7]` | `True` |

```{admonition} À retenir
:class: important

Pour **tester** l'égalité, on utilise `==` (deux signes égal).
Un seul `=` sert à **affecter** une valeur à une variable.

* `x = 5` : « `x` prend la valeur 5 » (affectation) ;
* `x == 5` : « est-ce que `x` vaut 5 ? » (comparaison, qui donne `True` ou `False`).
```

Les comparaisons fonctionnent aussi avec les chaînes de caractères :

```{code-cell}
prenom = "Aude"
print(prenom == "Aude")
print(prenom == "aude")   # attention, la casse compte !
print("a" < "b")          # ordre alphabétique
```

### Combiner des conditions : `and`, `or`, `not`

On peut combiner plusieurs conditions à l'aide des opérateurs logiques :

* `A and B` est vrai si **A et B sont tous les deux vrais** ;
* `A or B` est vrai si **au moins l'un des deux** est vrai ;
* `not A` est vrai si A est faux (et inversement).

```{code-cell}
age = 20
etudiant = True
print(age >= 18 and etudiant)   # majeur ET étudiant
print(age < 12 or age > 65)     # enfant OU senior
print(not etudiant)
```

Pour tester si une valeur est comprise dans un intervalle, Python autorise une écriture proche des mathématiques :

```{code-cell}
note = 14
print(10 <= note < 20)   # équivaut à 10 <= note and note < 20
```

```{admonition} Testez-vous
:class: hint

Avec `a = 3` et `b = 8`, que valent les expressions suivantes ?

1. `a > 2 and b > 10`
2. `a > 2 or b > 10`
3. `not (a == 3)`
4. `a != b`
5. `a < b < 5`
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

1. `False` : `a > 2` est vrai mais `b > 10` est faux, et `and` exige que les deux soient vrais ;
2. `True` : il suffit que l'une des deux conditions soit vraie ;
3. `False` : `a == 3` est vrai, donc sa négation est fausse ;
4. `True` ;
5. `False` : `a < b` est vrai mais `b < 5` est faux.
```

```{raw} latex
\fi
```

## L'instruction `if`

Pour n'exécuter des instructions que si une condition est vraie, on utilise le mot-clé `if` (« si » en anglais) :

```{code-cell}
x = 12
if x > 0:
    print("x est positif")
    print("x n'est pas négatif")
print("Fin du programme")
```

Observez bien la syntaxe :

* la ligne du `if` se termine par **deux-points** `:` ;
* les instructions à exécuter si la condition est vraie sont **indentées**, c'est-à-dire décalées vers la droite (de 4 espaces, ou d'une tabulation) : elles forment un **bloc** ;
* le bloc se termine dès qu'une ligne revient au niveau d'indentation du `if` : ici, `print("Fin du programme")` est exécutée dans tous les cas.

Si l'on change la valeur de `x` pour une valeur négative, seule la dernière ligne est exécutée :

```{code-cell}
x = -3
if x > 0:
    print("x est positif")
    print("x n'est pas négatif")
print("Fin du programme")
```

```{admonition} À retenir : l'indentation
:class: important

Dans beaucoup de langages, l'indentation n'est qu'une convention de présentation.
**En Python, elle fait partie de la syntaxe** : c'est elle qui indique à Python où commence et où se termine un bloc.
Un mauvais décalage change le sens du programme, ou provoque une erreur.
La plupart des éditeurs (dont Thonny) indentent automatiquement après un `:` ; utilisez la touche Tab et évitez de mélanger tabulations et espaces.
```

```{admonition} Testez-vous
:class: hint

Qu'affichent ces deux programmes, qui ne diffèrent que par l'indentation de la dernière ligne ?

    # Programme A               # Programme B
    note = 8                    note = 8
    if note >= 10:              if note >= 10:
        print("Admis")              print("Admis")
        print("Bravo")          print("Bravo")
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

Le programme A n'affiche **rien** : la condition est fausse et les deux `print` font partie du bloc du `if`.

Le programme B affiche `Bravo` : le second `print` n'est pas indenté, il ne fait donc pas partie du bloc et il est exécuté dans tous les cas (ce qui n'est sans doute pas ce que l'on voulait !).
```

```{raw} latex
\fi
```

## `else` : sinon…

Souvent, on veut exécuter un bloc si la condition est vraie, et **un autre bloc sinon**.
On utilise alors le mot-clé `else` (« sinon ») :

```{code-cell}
note = 8
if note >= 10:
    print("Admis")
else:
    print("Ajourné")
```

Le mot-clé `else` est placé **au même niveau d'indentation que le `if`** auquel il se rapporte, suivi lui aussi de `:`.
Un seul des deux blocs est exécuté, jamais les deux.

## `elif` : sinon si…

Lorsqu'il y a plus de deux cas, on enchaîne les tests avec `elif` (contraction de _else if_, « sinon si ») :

```{code-cell}
t = 25
if t <= 0:
    print("L'eau est solide")
elif t < 100:
    print("L'eau est liquide")
else:
    print("L'eau est gazeuse")
```

Python teste les conditions **dans l'ordre** et exécute **uniquement le bloc de la première condition vraie** ; si aucune n'est vraie, c'est le bloc `else` (facultatif) qui est exécuté.

```{figure} ../img/fig_if.*
:width: 80%

Le chemin suivi par le programme précédent pour `t = 25` : la première condition est fausse, la deuxième est vraie, on affiche donc « liquide » et on ignore la suite.
```

*[Voir ce code s'exécuter pas à pas dans Python Tutor](https://pythontutor.com/visualize.html#code=t%20%3D%2025%0Aif%20t%20%3C%3D%200%3A%0A%20%20%20%20print%28%22L%27eau%20est%20solide%22%29%0Aelif%20t%20%3C%20100%3A%0A%20%20%20%20print%28%22L%27eau%20est%20liquide%22%29%0Aelse%3A%0A%20%20%20%20print%28%22L%27eau%20est%20gazeuse%22%29%0A&cumulative=false&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D&textReferences=false)*

Remarquez qu'on n'a pas eu besoin d'écrire `elif t > 0 and t < 100` : si l'on arrive au `elif`, c'est que la condition `t <= 0` était fausse, donc que `t > 0`.

```{admonition} Erreur fréquente : l'ordre des tests
:class: warning

Comme seule la **première** condition vraie compte, l'ordre des tests est important.
Que penser du programme suivant, censé attribuer une mention ?

    note = 17
    if note >= 10:
        print("Passable")
    elif note >= 14:
        print("Bien")
    elif note >= 16:
        print("Très bien")

Il affiche `Passable` pour une note de 17 ! En effet, la première condition (`note >= 10`) est vraie, donc les suivantes ne sont même pas testées.
Il faut tester les conditions **de la plus restrictive à la moins restrictive** : d'abord `note >= 16`, puis `note >= 14`, puis `note >= 10`.
```

```{admonition} Testez-vous
:class: hint

Qu'affiche ce programme pour `x = 5` ? Pour `x = -1` ? Pour `x = 0` ?

    if x > 0:
        print("A")
    elif x > -2:
        print("B")
    else:
        print("C")
    print("D")
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

* Pour `x = 5` : `A` puis `D` ;
* pour `x = -1` : `B` puis `D` (la première condition est fausse, la seconde est vraie) ;
* pour `x = 0` : `B` puis `D` (0 n'est pas strictement positif, mais il est bien plus grand que -2).

Dans tous les cas, `D` est affiché puisque cette ligne ne fait partie d'aucun bloc.
```

```{raw} latex
\fi
```

## Conditions imbriquées

Un bloc peut lui-même contenir un `if` : on parle de conditions **imbriquées**.
Chaque niveau d'imbrication ajoute un niveau d'indentation.

```{code-cell}
age = 20
etudiant = True
if age >= 18:
    if etudiant:
        print("Tarif étudiant : 5 euros")
    else:
        print("Plein tarif : 9 euros")
else:
    print("Tarif enfant : 4 euros")
```

Lorsque c'est possible, on préfère toutefois éviter les imbrications trop profondes, qui rendent le code difficile à lire : un `and` ou un `elif` permettent souvent de « mettre à plat » la structure.

```{admonition} Erreurs fréquentes de ce chapitre
:class: warning

| Message d'erreur | Cause probable |
|---|---|
| `SyntaxError: expected ':'` | les deux-points oubliés à la fin d'une ligne `if`, `elif` ou `else` |
| `IndentationError: expected an indented block` | la ligne qui suit un `:` n'est pas indentée |
| `IndentationError: unexpected indent` | une ligne est indentée alors qu'elle ne devrait pas l'être |
| `IndentationError: unindent does not match any outer indentation level` | les décalages ne sont pas cohérents (par exemple 4 espaces puis 3) |
| `SyntaxError: invalid syntax` sur un `if x = 5:` | `=` utilisé à la place de `==` dans une condition (les versions récentes de Python suggèrent même : _Maybe you meant '==' …_) |
| `SyntaxError: invalid syntax` sur un `else` | `else` mal aligné avec son `if`, ou `else` suivi d'une condition (`else x > 5:` est interdit : utiliser `elif`) |
```

Voici par exemple l'erreur obtenue en oubliant d'indenter le contenu d'un bloc :

```{code-cell}
:tags: [raises-exception]
x = 3
if x > 0:
print("positif")
```

````{admonition} Si vous venez de R ou de SAS
:class: seealso

* Les blocs sont délimités par l'**indentation** et non par des accolades (`{ }` en R) ou par `DO; ... END;` (en SAS) : c'est la différence de syntaxe qui surprend le plus au début.
* `else if` s'écrit `elif`, et chaque ligne `if`, `elif`, `else` se termine par `:`.
* Les opérateurs logiques s'écrivent en toutes lettres : `and`, `or`, `not` (au lieu de `&&`, `||`, `!` en R). Attention : avec `pandas`, pour combiner des conditions sur des colonnes entières, on utilisera `&`, `|` et `~` (chapitre 11), comme `&` et `|` en R.
* Le test d'égalité est `==` (comme en R, et non `=` comme dans une instruction `IF` de SAS).
````

## Exemple guidé : le prix d'un billet de train

Avant de passer aux exercices, voyons sur un exemple comment aborder un problème.

_Énoncé : un billet de train coûte 40 €. Les moins de 12 ans paient demi-tarif, les 12–25 ans ont 30 % de réduction, les plus de 60 ans ont 20 % de réduction. Calculer et afficher le prix du billet en fonction de l'âge._

**Étape 1 : identifier les cas.** Faisons la liste des situations possibles, sur un axe des âges :

* moins de 12 ans : 50 % de réduction ;
* de 12 à 25 ans : 30 % ;
* de 26 à 60 ans : aucune réduction ;
* plus de 60 ans : 20 %.

Les cas ne se chevauchent pas et couvrent tous les âges : une structure `if` / `elif` / `else` convient parfaitement.

**Étape 2 : choisir des exemples de test _avant_ de programmer.** Pour 8 ans, on attend 20 € ; pour 25 ans, 28 € ; pour 40 ans, 40 € ; pour 70 ans, 32 €.
Testons aussi les cas « limites » : 12 ans (28 €) et 60 ans (40 €, car « plus de 60 ans » signifie strictement plus).

**Étape 3 : écrire le code.**

```{code-cell}
age = 25
prix_plein = 40

if age < 12:
    reduction = 0.5
elif age <= 25:
    reduction = 0.3
elif age <= 60:
    reduction = 0
else:
    reduction = 0.2

prix = prix_plein * (1 - reduction)
print(f"À {age} ans, le billet coûte {prix:.2f} euros")
```

**Étape 4 : tester** avec toutes les valeurs choisies à l'étape 2 en modifiant la première ligne. Essayez !

Remarquez l'astuce : plutôt que d'écrire quatre fois le calcul et le `print`, on calcule seulement le **taux de réduction** dans les différents cas, puis on fait le calcul une seule fois à la fin.

## Exercices

(ex2.1)=
```{admonition} Exercice 2.1 : Pair ou impair ★
Écrivez un programme qui, pour un entier stocké dans une variable `n`, affiche `n est pair` ou `n est impair` (avec la valeur de `n` à la place de la lettre `n`).
```

<div id="pad_2_1" class="pad"></div>
<script>
    Pythonpad('pad_2_1', {'id': 'aude_2.1', 'title': 'Testez votre code ici', 'src': "n = 7\n# Complétez ce code\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Un nombre est pair si le reste de sa division par 2 est nul. Relisez la section sur l'opérateur `%` au chapitre 1.
```

````{admonition} Solution
:class: tip, dropdown

```python
n = 7
if n % 2 == 0:
    print(f"{n} est pair")
else:
    print(f"{n} est impair")
```
````

```{raw} latex
\fi
```

(ex2.2)=
```{admonition} Exercice 2.2 : Température de l'eau ★
Écrivez une structure conditionnelle qui, à partir d'une température d'eau stockée dans une variable `t`, affiche si l'eau à cette température est à l'état solide, liquide ou gazeux.
Contrairement à l'exemple du cours, testez les conditions en commençant par l'état gazeux.
```

<div id="pad_2_2" class="pad"></div>
<script>
    Pythonpad('pad_2_2', {'id': 'aude_2.2', 'title': 'Testez votre code ici', 'src': "t = -3\n# Complétez ce code\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
t = -3
if t >= 100:
    print("l'eau est sous forme gazeuse")
elif t > 0:
    print("l'eau est sous forme liquide")
else:
    print("l'eau est sous forme solide")
```

Testez les valeurs limites : 0 (solide), 0.5 (liquide), 100 (gazeux).
````

```{raw} latex
\fi
```

(ex2.3)=
```{admonition} Exercice 2.3 : Mention ★★
Écrivez un programme qui, à partir d'une note sur 20 stockée dans `note`, affiche la mention correspondante :
« Ajourné » (moins de 10), « Passable » (de 10 inclus à 12 exclu), « Assez bien » (de 12 à 14), « Bien » (de 14 à 16), « Très bien » (16 et plus).
Si la note n'est pas comprise entre 0 et 20, le programme doit afficher « Note invalide ».
```

<div id="pad_2_3" class="pad"></div>
<script>
    Pythonpad('pad_2_3', {'id': 'aude_2.3', 'title': 'Testez votre code ici', 'src': "note = 13.5\n# Complétez ce code\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Commencez par traiter le cas « Note invalide » (avec un `or`), puis enchaînez des `elif` en allant de la meilleure mention à la moins bonne (ou l'inverse, mais alors avec des `<`).
```

````{admonition} Solution
:class: tip, dropdown

```python
note = 13.5
if note < 0 or note > 20:
    print("Note invalide")
elif note >= 16:
    print("Très bien")
elif note >= 14:
    print("Bien")
elif note >= 12:
    print("Assez bien")
elif note >= 10:
    print("Passable")
else:
    print("Ajourné")
```
````

```{raw} latex
\fi
```

(ex2.4)=
```{admonition} Exercice 2.4 : Le plus grand de trois nombres ★★
Écrivez un programme qui affiche le plus grand de trois nombres stockés dans les variables `a`, `b` et `c`, **sans utiliser la fonction `max`** de Python.
Testez votre programme en faisant varier la position du plus grand nombre (en `a`, en `b`, puis en `c`) et avec des valeurs égales.
```

<div id="pad_2_4" class="pad"></div>
<script>
    Pythonpad('pad_2_4', {'id': 'aude_2.4', 'title': 'Testez votre code ici', 'src': "a = 4\nb = 11\nc = 7\n# Complétez ce code\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Première idée : `a` est le plus grand si `a >= b and a >= c`.
Seconde idée (plus facile à généraliser) : utilisez une variable `plus_grand` qui vaut d'abord `a`, puis comparez-la successivement à `b` et à `c`.
```

````{admonition} Solution
:class: tip, dropdown

Avec des conditions combinées :

```python
a = 4
b = 11
c = 7
if a >= b and a >= c:
    print(a)
elif b >= c:   # ici, on sait que a n'est pas le plus grand
    print(b)
else:
    print(c)
```

Avec une variable intermédiaire :

```python
a = 4
b = 11
c = 7
plus_grand = a
if b > plus_grand:
    plus_grand = b
if c > plus_grand:
    plus_grand = c
print(plus_grand)
```

Notez que la seconde version utilise deux `if` **indépendants** (et non un `elif`) : il faut bien effectuer les deux comparaisons.
Nous reverrons cette idée pour trouver le plus grand élément d'une liste.
````

```{raw} latex
\fi
```

(ex2.5)=
```{admonition} Exercice 2.5 : Année bissextile ★★★
Une année est bissextile si elle est divisible par 4 mais pas par 100, ou si elle est divisible par 400.
Ainsi, 2024 et 2000 sont bissextiles, mais 1900 et 2023 ne le sont pas.
Écrivez un programme qui affiche si l'année stockée dans `annee` est bissextile.
```

<div id="pad_2_5" class="pad"></div>
<script>
    Pythonpad('pad_2_5', {'id': 'aude_2.5', 'title': 'Testez votre code ici', 'src': "annee = 1900\n# Complétez ce code\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

« `annee` est divisible par 4 » s'écrit `annee % 4 == 0`.
Traduisez ensuite la phrase de l'énoncé avec `and`, `or` et des parenthèses : `(... and ...) or ...`.
```

````{admonition} Solution
:class: tip, dropdown

```python
annee = 1900
if (annee % 4 == 0 and annee % 100 != 0) or annee % 400 == 0:
    print(annee, "est bissextile")
else:
    print(annee, "n'est pas bissextile")
```

Testez avec 2024, 2000, 1900 et 2023 : ce sont les quatre cas « types ». Nous reviendrons sur cet exemple au chapitre 8 pour apprendre à tester son code de manière systématique.
````

```{raw} latex
\fi
```

## Bilan du chapitre

```{admonition} À retenir
:class: important

* Une condition vaut `True` ou `False`. Opérateurs : `<`, `>`, `<=`, `>=`, `==`, `!=`, `in`, combinés avec `and`, `or`, `not`.
* `==` compare, `=` affecte.
* Syntaxe :

      if condition1:
          bloc exécuté si condition1 est vraie
      elif condition2:
          bloc exécuté si condition1 est fausse et condition2 vraie
      else:
          bloc exécuté si aucune condition n'est vraie

* Les deux-points `:` et l’**indentation** sont obligatoires.
* Seul le bloc de la **première** condition vraie est exécuté : l'ordre des tests compte.
```

Faites le point : êtes-vous capable de…

- prédire la valeur (`True` ou `False`) d'une condition combinant `and`, `or` et `not` ?
- écrire un `if` / `elif` / `else` correctement indenté ?
- expliquer pourquoi l'ordre des `elif` est important ?
- choisir des valeurs de test, y compris des cas limites, pour vérifier votre programme ?
- corriger une `IndentationError` ?
