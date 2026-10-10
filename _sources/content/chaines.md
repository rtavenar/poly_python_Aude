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

(ch:chaines)=
# Les chaînes de caractères

```{admonition} Objectifs du chapitre
:class: note

À la fin de ce chapitre, vous saurez :

* manipuler une chaîne de caractères comme une liste de caractères (indices, sous-chaînes, parcours) ;
* convertir des chaînes en nombres et inversement ;
* utiliser les principales méthodes des chaînes (`split`, `lower`, `replace`, `strip`…) ;
* mettre en forme des affichages avec `format` et les f-strings.

**Prérequis :** chapitres 1 à 5. **Durée indicative :** 1h30.
```

Nous nous intéressons maintenant plus en détail à un type de données que nous utilisons depuis le début : les chaînes de caractères (type `str`).
Pour créer une chaîne de caractères, il suffit d'utiliser des guillemets, simples ou doubles (les deux sont équivalents) :

```{code-cell}
s1 = "abc"
s2 = 'bde'
s3 = "L'apostrophe passe sans problème entre guillemets doubles"
print(s3)
```

Comme pour les listes, il est conseillé de se reporter à [la documentation en ligne](https://docs.python.org/fr/3/library/stdtypes.html#string-methods) lorsque vous avez des doutes sur la manipulation des chaînes de caractères.

## Conversion d'une chaîne en nombre

Si une chaîne de caractères représente une valeur numérique (comme la chaîne `"10.2"`), on peut la transformer en entier ou en nombre à virgule pour l'utiliser ensuite dans des calculs, avec les fonctions de conversion `int` et `float`.
C'est indispensable lorsque les données proviennent d'un fichier ou d'une saisie de l'utilisateur, qui sont toujours lues sous forme de texte.

```{code-cell}
s = "10.2"
f = float(s)
print(f + 2)
print(f == s)   # un nombre n'est jamais égal à une chaîne
```

```{code-cell}
s = "10"
i = int(s)
print(i - 1)
print(s * 2)   # attention : sur une chaîne, * répète !
```

## Analogie avec les listes

Une chaîne de caractères se manipule en partie comme une liste de caractères.
On peut ainsi obtenir sa longueur avec `len`, ou accéder à son $i$-ème caractère avec la notation `s[i]`, y compris avec des indices négatifs :

```{figure} ../img/fig_indices_chaine.*
:width: 65%

Les indices des caractères de la chaîne `"Python"`.
```

```{code-cell}
s = "Python"
print(len(s))
print(s[0])
print(s[-1])
```

De même, on peut extraire des sous-chaînes à partir des indices de début et de fin (exclu) :

```{code-cell}
print(s[2:4])
print(s[:2])
```

On peut aussi parcourir une chaîne caractère par caractère avec une boucle `for` :

```{code-cell}
for lettre in "abc":
    print(lettre)
```

Comme pour les listes, on peut concaténer deux chaînes avec l'opérateur `+` et répéter une chaîne avec l'opérateur `*` :

```{code-cell}
s = "ab" + ("cde" * 3)
print(s)
```

Enfin, le mot-clé `in` permet de tester la présence d'une sous-chaîne dans une chaîne :

```{code-cell}
s = "abcde"
print("a" in s)
print("bcd" in s)
print("bCd" in s)
```

```{admonition} À retenir : les chaînes ne sont pas modifiables
:class: important

L'analogie entre listes et chaînes de caractères n'est pas parfaite.
En particulier, on peut **lire** le $i$-ème caractère d'une chaîne, mais **pas le modifier** : si `s` est une chaîne de caractères, l'instruction `s[2] = "c"` provoque une erreur.
On dit que les chaînes sont **non modifiables** (ou _immuables_).
Pour « modifier » une chaîne, on en construit une nouvelle, que l'on peut ranger dans la même variable :
```

```{code-cell}
:tags: [raises-exception]
s = "maison"
s[0] = "r"
```

```{code-cell}
s = "maison"
s = "r" + s[1:]   # on construit une nouvelle chaîne
print(s)
```

```{admonition} Testez-vous
:class: hint

Avec `mot = "bonjour"`, que valent : `mot[3]`, `mot[-2]`, `mot[1:4]`, `len(mot)`, `mot[0] + mot[-1]` et `"jour" in mot` ?
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

* `mot[3]` vaut `"j"` ;
* `mot[-2]` vaut `"u"` ;
* `mot[1:4]` vaut `"onj"` ;
* `len(mot)` vaut `7` ;
* `mot[0] + mot[-1]` vaut `"br"` ;
* `"jour" in mot` vaut `True`.
```

```{raw} latex
\fi
```

### Construire une chaîne petit à petit

De la même façon que l'on construit une liste avec `append`, on peut construire une chaîne en partant d'une chaîne vide `""` et en lui ajoutant des morceaux au fil d'une boucle :

```{code-cell}
mot = "python"
resultat = ""
for lettre in mot:
    resultat = resultat + lettre + "-"
print(resultat)
```

## Principales méthodes des chaînes

Les chaînes disposent de nombreuses **méthodes** (des fonctions propres au type `str`, appelées avec la syntaxe `chaine.methode(...)`).
Comme les chaînes ne sont pas modifiables, ces méthodes ne modifient jamais la chaîne d'origine : elles **retournent une nouvelle valeur**.

| Méthode | Description |
|---|---|
| `ch.lower()` | retourne la version en minuscules de `ch` |
| `ch.upper()` | retourne la version en majuscules de `ch` |
| `ch.strip()` | retourne `ch` sans les espaces (et retours à la ligne) au début et à la fin |
| `ch.replace(old, new)` | retourne une copie de `ch` où toutes les occurrences de `old` sont remplacées par `new` |
| `ch.split(sep)` | retourne la **liste** des morceaux de `ch` découpée à chaque occurrence de `sep` (par défaut, à chaque espace ou retour à la ligne) |
| `sep.join(liste)` | l'inverse de `split` : retourne la chaîne obtenue en collant les éléments de `liste` (des chaînes) séparés par `sep` |
| `ch.count(sub)` | retourne le nombre d'occurrences de `sub` dans `ch` |
| `ch.find(sub)` | retourne l'indice de la première occurrence de `sub` dans `ch` (ou -1 si `sub` n'est pas dans `ch`) |
| `ch.rfind(sub)` | retourne l'indice de la dernière occurrence de `sub` dans `ch` |
| `ch.startswith(prefix)` | retourne `True` si `ch` commence par `prefix` |
| `ch.endswith(suffix)` | retourne `True` si `ch` se termine par `suffix` |
| `ch.islower()`, `ch.isupper()` | retourne `True` si les lettres de `ch` sont toutes en minuscules (resp. majuscules) |
| `ch.isnumeric()` | retourne `True` si `ch` n'est constituée que de chiffres |
| `ch.format(...)` | remplace les `{}` de `ch` par les valeurs passées en argument (voir plus bas) |

Voici quelques exemples :

```{code-cell}
ch = "  La vie est belle  "
print(ch.strip())
print(ch.upper())
print(ch.replace("belle", "longue"))
print(ch.count("e"))
```

La méthode `split` est particulièrement utile pour découper un texte en mots, ou une ligne de données en champs :

```{code-cell}
phrase = "la vie est belle"
mots = phrase.split()
print(mots)
print(len(mots), "mots")

ligne = "Lemarchand;John;23"
print(ligne.split(";"))
```

et `join` fait l'opération inverse :

```{code-cell}
print("-".join(["2024", "09", "01"]))
print(" ".join(mots).upper())
```

```{admonition} Erreur fréquente
:class: warning

Les méthodes des chaînes **retournent** un résultat : elles ne modifient pas la chaîne.
Le code suivant n'a donc aucun effet visible :

    nom = "aude"
    nom.upper()
    print(nom)   # affiche toujours "aude"

Il faut récupérer le résultat : `nom = nom.upper()`.
```

```{admonition} Testez-vous
:class: hint

Que valent les expressions suivantes ?

1. `"Bonjour".lower().count("o")`
2. `"a,b,,c".split(",")`
3. `"Rennes".replace("n", "N")`
4. `"  x ".strip() + "!"`
5. `"".join(["a", "b", "c"])`
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

1. `2` (on peut enchaîner les méthodes : `"bonjour".count("o")`) ;
2. `['a', 'b', '', 'c']` (une chaîne vide apparaît entre les deux virgules consécutives) ;
3. `"ReNNes"` ;
4. `"x!"` ;
5. `"abc"`.
```

```{raw} latex
\fi
```

## Mettre en forme des chaînes de caractères

Nous avons vu au chapitre 1 deux façons d'insérer des valeurs de variables dans une chaîne : la méthode `format` et les f-strings.
Revenons-y plus en détail.

### La méthode `format`

La méthode `format` recherche dans la chaîne les accolades `{}` et les remplace, dans l'ordre, par les valeurs fournies :

```{code-cell}
age = 12
prenom = "Micheline"
s = "{} a {} ans".format(prenom, age)
print(s)
```

On peut aussi nommer les emplacements, ce qui est utile pour les chaînes longues contenant de nombreuses valeurs, et préciser le format d'affichage après un `:` (ici, 3 chiffres après la virgule) :

```{code-cell}
s = "{prenom} a {age:.3f} ans".format(prenom="Micheline", age=12)
print(s)
```

### Les f-strings

Les f-strings (pour _formatted strings_) sont une écriture plus concise du même principe : on place un `f` avant la chaîne et on écrit directement les variables, ou même des calculs, entre accolades :

```{code-cell}
age_chat = 12
s = f"Ce chat a {age_chat} ans, ce qui lui fait {age_chat * 6} ans en âge équivalent humain"
print(s)
```

### Les options de mise en forme

Que ce soit avec `format` ou avec une f-string, on peut ajouter après le nom de la variable un `:` suivi d'options de mise en forme, par exemple pour fixer le nombre de décimales ou aligner des valeurs en colonnes :

| Option | Effet | Exemple | Résultat |
|---|---|---|---|
| `:.2f` | 2 décimales | `f"{3.14159:.2f}"` | `3.14` |
| `:8.2f` | 2 décimales, largeur 8 | `f"{3.14159:8.2f}"` | `    3.14` |
| `:5d` | entier, largeur 5 | `f"{42:5d}"` | `   42` |
| `:<6` | aligné à gauche, largeur 6 | `f"{'ab':<6}"` | `ab    ` |
| `:>6` | aligné à droite, largeur 6 | `f"{'ab':>6}"` | `    ab` |
| `:^6` | centré, largeur 6 | `f"{'ab':^6}"` | `  ab  ` |

Vous trouverez une présentation exhaustive de ces options dans la [documentation Python](https://docs.python.org/fr/3/library/string.html#format-string-syntax).

## Exercices

(ex6.1)=
```{admonition} Exercice 6.1 : Compter les voyelles ★
Écrivez une fonction `nb_voyelles(s)` qui retourne le nombre de voyelles (a, e, i, o, u, y, en minuscules ou majuscules) contenues dans la chaîne `s`.
```

<div id="pad_6_1" class="pad"></div>
<script>
    Pythonpad('pad_6_1', {'id': 'aude_6.1', 'title': 'Testez votre code ici', 'src': "def nb_voyelles(s):\n    # Complétez ce code\n    pass\n\nprint(nb_voyelles(\"Bonjour Aude\"))  # doit afficher 6\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Parcourez la chaîne lettre par lettre, et testez si chaque lettre (mise en minuscule) est `in "aeiouy"`.
```

````{admonition} Solution
:class: tip, dropdown

```python
def nb_voyelles(s):
    compteur = 0
    for lettre in s.lower():
        if lettre in "aeiouy":
            compteur += 1
    return compteur

print(nb_voyelles("Bonjour Aude"))
```
````

```{raw} latex
\fi
```

(ex6.2)=
```{admonition} Exercice 6.2 : Mots commençant par un préfixe ★
Écrivez une fonction qui prend en argument deux chaînes de caractères `s` et `prefix` et retourne le nombre de mots de la chaîne `s` qui débutent par la chaîne `prefix`.
```

<div id="pad_6_2" class="pad"></div>
<script>
    Pythonpad('pad_6_2', {'id': 'aude_6.2', 'title': 'Testez votre code ici', 'src': "def compte_prefix(s, prefix):\n    # Complétez ce code\n    pass\n\nprint(compte_prefix(\"la vie est belle au bord du lac\", \"la\"))  # doit afficher 2\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
def compte_prefix(s, prefix):
    compteur = 0
    for mot in s.split():
        if mot.startswith(prefix):
            compteur += 1
    return compteur

print(compte_prefix("la vie est belle au bord du lac", "la"))
```
````

```{raw} latex
\fi
```

(ex6.3)=
```{admonition} Exercice 6.3 : Compter un mot sans tenir compte de la casse ★★
Écrivez une fonction qui prend en argument deux chaînes de caractères `s` et `mot_cible` et retourne le nombre d'occurrences du mot `mot_cible` dans la chaîne `s`, sans tenir compte de la casse (majuscules / minuscules).
Attention : on compte des **mots** entiers, `"la"` ne doit pas être compté dans `"lac"`.
```

<div id="pad_6_3" class="pad"></div>
<script>
    Pythonpad('pad_6_3', {'id': 'aude_6.3', 'title': 'Testez votre code ici', 'src': "def compte_sans_casse(s, mot_cible):\n    # Complétez ce code\n    pass\n\nprint(compte_sans_casse(\"La vie est LA aussi, au bord du lac\", \"la\"))  # doit afficher 2\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
def compte_sans_casse(s, mot_cible):
    compteur = 0
    mot_cible_minuscules = mot_cible.lower()
    for mot in s.split():
        if mot.lower() == mot_cible_minuscules:
            compteur += 1
    return compteur

print(compte_sans_casse("La vie est LA aussi, au bord du lac", "la"))
```

Remarquez que `s.count("la")` ne conviendrait pas : cette méthode compte les **sous-chaînes**, et trouverait donc aussi le « la » de « lac ».
````

```{raw} latex
\fi
```

(ex6.4)=
```{admonition} Exercice 6.4 : Acronyme ★★
Écrivez une fonction `acronyme(s)` qui retourne l'acronyme d'une expression, formé des premières lettres de chaque mot, en majuscules.
```

<div id="pad_6_4" class="pad"></div>
<script>
    Pythonpad('pad_6_4', {'id': 'aude_6.4', 'title': 'Testez votre code ici', 'src': "def acronyme(s):\n    # Complétez ce code\n    pass\n\nprint(acronyme(\"mathématiques et informatique appliquées aux sciences humaines et sociales\"))\n# doit afficher MEIAASHES\n"});
</script>

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
def acronyme(s):
    resultat = ""
    for mot in s.split():
        resultat += mot[0]
    return resultat.upper()

print(acronyme("mathématiques et informatique appliquées aux sciences humaines et sociales"))
```

(Dans la vraie vie, l'acronyme MIASHS ignore les petits mots comme « et » et « aux » : sauriez-vous modifier la fonction pour ignorer les mots de 3 lettres ou moins ?)
````

```{raw} latex
\fi
```

(ex6.5)=
```{admonition} Exercice 6.5 : Palindrome ★★
Un palindrome est un mot qui se lit de la même façon dans les deux sens, comme « radar » ou « kayak ».
Écrivez une fonction `est_palindrome(mot)` qui retourne `True` si `mot` est un palindrome.
En bonus, faites en sorte que la fonction ignore les espaces et la casse, pour reconnaître des phrases comme « Esope reste ici et se repose ».
```

<div id="pad_6_5" class="pad"></div>
<script>
    Pythonpad('pad_6_5', {'id': 'aude_6.5', 'title': 'Testez votre code ici', 'src': "def est_palindrome(mot):\n    # Complétez ce code\n    pass\n\nprint(est_palindrome(\"radar\"))   # doit afficher True\nprint(est_palindrome(\"python\"))  # doit afficher False\n"});
</script>

```{raw} latex
\iffalse
```

```{admonition} Indice
:class: hint, dropdown

Comparez `mot[i]` et `mot[len(mot) - 1 - i]` pour tous les `i` jusqu'au milieu du mot.
Ou bien construisez le mot à l'envers (voir l'exercice 5.3) et comparez-le au mot d'origine.
Pour le bonus, commencez par « nettoyer » la phrase avec `lower` et `replace`.
```

````{admonition} Solution
:class: tip, dropdown

```python
def est_palindrome(mot):
    n = len(mot)
    for i in range(n // 2):
        if mot[i] != mot[n - 1 - i]:
            return False
    return True

def est_palindrome_phrase(phrase):
    nettoyee = phrase.lower().replace(" ", "")
    return est_palindrome(nettoyee)

print(est_palindrome("radar"))
print(est_palindrome("python"))
print(est_palindrome_phrase("Esope reste ici et se repose"))
```
````

```{raw} latex
\fi
```

## Bilan du chapitre

```{admonition} À retenir
:class: important

* Une chaîne se manipule comme une liste de caractères **non modifiable** : `len(s)`, `s[i]`, `s[debut:fin]`, `for lettre in s`, `sous_chaine in s`.
* `int(s)`, `float(s)` convertissent une chaîne en nombre ; `str(x)` convertit en chaîne.
* Méthodes utiles : `lower`, `upper`, `strip`, `replace`, `split`, `join`, `count`, `find`, `startswith`, `endswith`. Elles **retournent** une nouvelle valeur.
* Mise en forme : `f"{x:.2f}"` (2 décimales).
```

Faites le point : êtes-vous capable de…

- extraire un caractère ou une sous-chaîne d'une chaîne ?
- parcourir une chaîne lettre par lettre, ou mot par mot avec `split` ?
- construire une nouvelle chaîne au fil d'une boucle ?
- expliquer pourquoi `s.upper()` seul ne modifie pas `s` ?
- afficher un nombre avec un nombre fixé de décimales ?
