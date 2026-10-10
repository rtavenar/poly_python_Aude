# Apprendre Python en autonomie

Version du polycopié _Introduction à Python_ (filière MIASHS, Université Rennes 2) réécrite pour Aude, afin qu'elle puisse apprendre en autonomie, avec pour objectif l'analyse de données : bases de Python, puis fichiers, `numpy`, `pandas`, `matplotlib`, `seaborn` et `statsmodels`. Aude connaissant R et SAS, chaque chapitre comporte des encadrés « Différences avec R et SAS » et des tables de correspondance.
Schémas, questions « Testez-vous », exercices progressifs (★ à ★★★) avec indices et corrections, encadrés « Erreurs fréquentes », bilans de fin de chapitre, mini-projets et fiche mémo.

## Structure

* `content/` : les chapitres (format MyST Markdown, Jupyter Book) et les fichiers de données utilisés dans les exemples (`simple.csv`, `entete.csv`, `simple.json`, `donnees/`).
* `content/donnees/` : `penguins.csv` (Palmer penguins, K. Gorman, licence CC0), `titanic.csv` et `flights.csv` (versions du dépôt `seaborn-data`), `notes.csv` (données fictives), `fable.txt` (La Fontaine).
* `img/` : les schémas, aux formats SVG (web) et PDF (LaTeX). Ils sont générés par `img/generer_figures.py` (`python img/generer_figures.py` depuis la racine pour les régénérer après modification).
* `_static/` : l'éditeur de code intégré (Pythonpad).

## Conventions dans les chapitres

* Les réponses, indices et solutions sont des encadrés repliables (`:class: tip, dropdown` / `hint, dropdown`), entourés de blocs `{raw} latex` `\iffalse` / `\fi` pour être masqués dans la version PDF.
* Les liens « Voir ce code s'exécuter pas à pas dans Python Tutor » contiennent le code encodé dans l'URL.
* Les fenêtres de code intégrées utilisent `Pythonpad` (identifiants `aude_<numéro d'exercice>`). Pythonpad repose sur Brython, sans `numpy` ni `pandas` : il n'y en a donc que dans les chapitres 1 à 8.

## Compilation

```
pip install -r requirements.txt
jupyter-book build .                                              # version web
jupyter-book build . --builder pdflatex --toc _toc_latex.yml     # version PDF
```

Licence : [CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/).
