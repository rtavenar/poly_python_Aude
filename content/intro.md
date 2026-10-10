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

# Bienvenue !

Ce document a été écrit **pour Aude**. C'est une version du polycopié _Introduction à Python_ de la filière MIASHS de l'Université de Rennes 2, **réécrite pour pouvoir apprendre seule, sans cours en présentiel**, avec un objectif précis : **acquérir les bases nécessaires pour analyser des données** (_data science_) avec Python.

Il vous mène des toutes premières lignes de code jusqu'à l'analyse d'un vrai jeu de données avec les bibliothèques `pandas`, `matplotlib`, `seaborn` et `statsmodels`.
Vous y trouverez :

* des **schémas** pour visualiser ce qui se passe dans la machine ;
* des questions **« Testez-vous »** au fil de la lecture, pour vérifier immédiatement que vous avez compris ;
* des **exercices progressifs** (de ★ à ★★★) avec des **indices** et des **corrections détaillées** ;
* des encadrés **« Erreurs fréquentes »** qui montrent les vrais messages d'erreur de Python et comment les corriger ;
* un **bilan** à la fin de chaque chapitre pour faire le point sur ce que vous savez faire ;
* des **mini-projets** pour mettre tout cela en pratique et une **fiche mémo** pour réviser.

Ce document est distribué librement sous licence [CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Le polycopié d'origine a notamment bénéficié des apports d'Aurélie Lemaitre, d'Agnès Maunoury et de Jean-Christophe Burnel.
N'hésitez pas à faire vos remarques à son auteur dont vous trouverez le contact sur [sa page web](https://rtavenar.github.io/).

## Un document fait pour Aude

Aude connaît déjà R et SAS : la logique de l'analyse de données (tableaux, variables, modèles statistiques) lui est donc familière. Ce qu'il reste à apprendre, c'est la **syntaxe** et les **habitudes** de Python, qui diffèrent sur des points importants. Le document en tient compte :

* des encadrés **« Différences avec R et SAS »** signalent, dans chaque chapitre, les pièges à éviter (indices qui commencent à 0, indentation, `return` obligatoire, copie des listes…) et donnent des **tables de correspondance** entre R, SAS et Python ;
* les chapitres 1 à 8 peuvent être parcourus plus vite : lisez les encadrés « À retenir » et « Différences avec R et SAS », répondez aux questions « Testez-vous », et faites au moins les exercices ★★. Ne les sautez pas complètement : `pandas` repose entièrement sur ces bases, et la plupart des erreurs viennent de réflexes R ou SAS appliqués à Python ;
* le chapitre 14 montre comment retrouver les modèles habituels (`lm`, `glm`, `PROC REG`, `PROC LOGISTIC`, tests…) avec `statsmodels` et `scipy`.

Apprendre un nouveau langage, c'est un peu comme apprendre une nouvelle langue étrangère : on progresse surtout en pratiquant régulièrement.

## Le parcours proposé

Les chapitres sont conçus pour être lus **dans l'ordre**, chacun s'appuyant sur les précédents.
Les durées indiquées sont des estimations (lecture + exercices) : prenez le temps qu'il vous faut !

| Partie | Chapitre | Durée indicative |
|---|---|---|
| Les bases de Python | 1. Variables, types et opérations | 1h30 |
| | 2. Les conditions | 1h30 |
| | 3. Les boucles | 2h |
| | 4. Les fonctions et les modules | 2h |
| Les collections de données | 5. Les listes | 2h30 |
| | 6. Les chaînes de caractères | 1h30 |
| | 7. Dictionnaires, _tuples_ et _sets_ | 2h |
| | 8. Déboguer et tester son code | 1h |
| Analyser des données | 9. Lire et écrire des fichiers | 1h30 |
| | 10. `numpy` et le calcul matriciel | 1h30 |
| | 11. Découvrir ses données avec `pandas` | 2h30 |
| | 12. Préparer et résumer ses données avec `pandas` | 2h30 |
| | 13. Visualiser ses données avec `matplotlib` et `seaborn` | 2h |
| | 14. Modélisation statistique avec `statsmodels` | 2h |
| S'entraîner | Mini-projets | 2h à 4h chacun |

Les chapitres 1 à 8 forment le **socle** de programmation : ne les négligez pas, même si vous avez hâte d'analyser des données ! `pandas` repose entièrement sur ces notions (variables, fonctions, listes, dictionnaires…), et la plupart des difficultés rencontrées plus tard viennent de bases fragiles.
Les chapitres 9 à 14 vous donnent ensuite les outils de l'analyse de données, que vous mettrez en œuvre dans les mini-projets.

```{admonition} Conseil
:class: tip

Plutôt que de faire 10 heures d'un coup, préférez des séances régulières de 1h à 2h (par exemple 3 fois par semaine).
Au début de chaque séance, relisez rapidement le **bilan** du chapitre précédent.
```

## Comment lire les encadrés

Tout au long de ce document, vous rencontrerez différents types d'encadrés.
Voici à quoi ils ressemblent et ce qu'ils signifient.

```{admonition} Objectifs du chapitre
:class: note

Au début de chaque chapitre : ce que vous saurez faire à la fin.
```

```{admonition} À retenir
:class: important

Les points essentiels, à connaître par cœur.
```

```{admonition} Erreur fréquente
:class: warning

Les pièges dans lesquels (presque) tout le monde tombe au début, et comment s'en sortir.
```

```{admonition} Testez-vous
:class: hint

Une petite question pour vérifier votre compréhension.
Essayez **vraiment** d'y répondre (dans votre tête ou sur papier) avant de déplier la réponse.
```

```{admonition} Réponse
:class: tip, dropdown

La réponse apparaît quand on clique sur le titre de l'encadré.
```

```{admonition} Exercice 0.1 ★
Un exercice à faire sur ordinateur. Le nombre d'étoiles indique la difficulté :

* ★ : application directe du cours ;
* ★★ : demande de combiner plusieurs notions ou de réfléchir un peu ;
* ★★★ : plus difficile, pour aller plus loin (ne vous découragez pas si vous bloquez !).
```

```{admonition} Indice
:class: hint, dropdown

Un coup de pouce si vous êtes bloquée. N'ouvrez l'indice qu'après avoir cherché un moment.
```

```{admonition} Solution
:class: tip, dropdown

Une correction commentée. Il y a souvent plusieurs bonnes solutions : si la vôtre est différente mais donne le bon résultat, elle est sans doute correcte aussi !
```

```{admonition} Pour aller plus loin
:class: seealso

Des compléments facultatifs, que vous pouvez sauter lors d'une première lecture.
```

```{raw} latex
\iffalse
```

Les indices, réponses et solutions sont repliés : cliquez sur le titre de l'encadré pour les afficher.

```{raw} latex
\fi
```

```{raw} latex
Dans cette version PDF, les réponses, indices et solutions sont masqués : vous les trouverez (repliés) dans la version web de ce document.
```

## Où écrire et exécuter du code Python ?

### Les blocs de code de ce document

Durant la lecture, vous trouverez des blocs de code tels que celui-ci :

```{code-cell}
def f(v):
    return v ** 2

x = 5
y = f(3 * x + 2)
print(y)
```

Le bloc situé sous le code correspond à ce qu'affiche ce code lorsqu'on l'exécute.

```{admonition} À retenir
:class: important

**Ne vous contentez pas de lire les exemples : retapez-les vous-même**, exécutez-les, puis modifiez-les pour voir ce qui change.
C'est de loin la meilleure façon d'apprendre.
Évitez le copier-coller, qui donne l'illusion d'avoir compris : taper le code vous oblige à faire attention à chaque détail (parenthèses, deux-points, décalages…).
```

### Option 1 : les fenêtres de code intégrées (version web)

Dans la version web de ce document, vous trouverez des fenêtres d'éditeur de code vous permettant de tester vos solutions aux exercices directement dans votre navigateur, sans rien installer.
En voici une : appuyez sur « Run » pour exécuter le code, puis modifiez le code et observez le résultat en le ré-exécutant.

<div id="pad_intro" class="pad"></div>
<script>
    Pythonpad('pad_intro', {'id': 'aude_intro', 'title': 'Testez votre code ici', 'src': "a = 12 * 5\nprint(a)\nprint(\"Bonjour !\")\n"});
</script>

### Option 2 : sans installation, dans le navigateur

Si vous ne pouvez pas installer de logiciel, le site [Basthon](https://basthon.fr) propose une console et des carnets (_notebooks_) Python qui fonctionnent directement dans le navigateur.

### Option 3 (recommandée) : installer Python sur votre ordinateur

Pour travailler confortablement, il est préférable d'installer Python sur votre ordinateur. Deux outils sont utiles, selon la partie du document :

* **Pour les chapitres 1 à 9**, le logiciel [Thonny](https://thonny.org) est idéal pour débuter : il est gratuit, disponible sous Windows, macOS et Linux, et il installe Python en même temps que lui. Son interface est très simple : une zone **éditeur** (en haut) pour écrire un programme et l'enregistrer dans un fichier `.py`, un bouton **Run** (triangle vert) pour l'exécuter, et une **console** (en bas) où s'affichent les résultats. Thonny peut aussi afficher les valeurs de vos variables (menu _View > Variables_), ce qui est très pratique pour comprendre ce que fait un programme.
* **Pour l'analyse de données (chapitres 10 à 14 et projets)**, on travaille dans des **notebooks Jupyter** : des documents qui mêlent cellules de code, résultats (tableaux, graphiques) et texte, ce qui est idéal pour explorer des données et garder une trace de son analyse. Le plus simple est d'installer la distribution [Anaconda](https://www.anaconda.com/download), qui contient Python, Jupyter, `numpy`, `pandas`, `matplotlib`, `seaborn`, `statsmodels` et `scipy`. Vous pouvez aussi utiliser [Google Colab](https://colab.research.google.com), qui fait fonctionner des notebooks dans le navigateur, sans installation, avec toutes ces bibliothèques (un compte Google est nécessaire).

Rien ne vous empêche d'utiliser Jupyter dès le début, si vous préférez un seul outil.

```{admonition} Les fichiers de données
:class: tip

Plusieurs chapitres utilisent des fichiers de données (dans le dossier `donnees` qui accompagne ce document) : `notes.csv`, `fable.txt`, et trois jeux de données réels très utilisés pour apprendre l'analyse de données : `penguins.csv` (des manchots de l'Antarctique), `titanic.csv` (des passagers du Titanic) et `flights.csv` (le trafic d'une compagnie aérienne de 1949 à 1960).
Placez votre notebook ou votre script dans le même dossier que le dossier `donnees`.
```

```{admonition} Console ou fichier ?
:class: seealso

Il y a deux façons de faire exécuter du code Python :

1. dans une **console** (le prompt `>>>`) : chaque instruction est exécutée dès que vous appuyez sur Entrée. C'est pratique pour faire de petits essais ;
2. dans un **fichier** `.py` (un _script_) que l'on fait exécuter en entier. C'est ce que l'on fait dès que le programme fait plus de quelques lignes, car on garde une trace de ce que l'on a écrit.

En ligne de commande (dans un terminal), on lance la console avec `python` (ou `python3`) et on exécute un script avec `python nom_de_mon_fichier.py`.
Assurez-vous d'utiliser Python 3 (la console affiche sa version au démarrage) : ce document ne s'applique pas à Python 2, qui n'est plus utilisé.
```

### Un outil précieux : Python Tutor

Certains exemples de ce document sont accompagnés d'un lien _« Voir ce code s'exécuter pas à pas dans Python Tutor »_.
Le site [Python Tutor](https://pythontutor.com) permet d'exécuter un programme **instruction par instruction** (bouton _Next_) en dessinant à chaque étape les variables et leurs valeurs.
C'est l'équivalent d'un enseignant qui expliquerait au tableau ce qui se passe dans la machine : n'hésitez pas à l'utiliser dès qu'un code vous semble mystérieux, y compris le vôtre !

Voici un premier exemple à essayer :

```python
prenom = "Aude"
age = 20
age = age + 1
print(prenom, "a", age, "ans")
```

*[Voir ce code s'exécuter pas à pas dans Python Tutor](https://pythontutor.com/visualize.html#code=prenom%20%3D%20%22Aude%22%0Aage%20%3D%2020%0Aage%20%3D%20age%20%2B%201%0Aprint%28prenom%2C%20%22a%22%2C%20age%2C%20%22ans%22%29%0A&cumulative=false&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D&textReferences=false)*

## Méthode de travail conseillée

Pour chaque chapitre :

1. **Lisez les objectifs** pour savoir où vous allez.
2. **Lisez une section** en retapant et en exécutant les exemples. Modifiez-les : que se passe-t-il si… ?
3. **Répondez aux questions « Testez-vous »** avant de regarder la réponse. Si vous vous êtes trompée, relisez la section : c'est normal et c'est comme ça qu'on apprend.
4. **Faites les exercices** dans l'ordre. Cherchez au moins 10 à 15 minutes avant d'ouvrir l'indice, puis encore un peu avant d'ouvrir la solution. Une fois la solution lue, **refaites l'exercice sans la regarder**.
5. **Faites le bilan** en fin de chapitre : cochez ce que vous savez faire et revenez sur ce qui reste flou.

```{admonition} Que faire quand on est bloquée ?
:class: tip

1. **Lisez le message d'erreur** en entier, et en particulier sa dernière ligne (nous apprendrons à les lire dès le chapitre 1).
2. **Affichez vos variables** avec `print` à différents endroits du programme pour vérifier qu'elles contiennent ce que vous croyez.
3. **Exécutez votre code pas à pas** dans Python Tutor ou dans Thonny.
4. **Expliquez votre code à voix haute**, ligne par ligne, comme si vous l'expliquiez à quelqu'un d'autre (même à un canard en plastique : c'est une technique reconnue chez les programmeurs !). On trouve souvent l'erreur en cours de route.
5. **Faites une pause.** Sérieusement : la solution vient souvent après.
```

C'est parti !
