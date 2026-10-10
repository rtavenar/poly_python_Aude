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

(ch:et_apres)=
# Et après ?

Félicitations, vous êtes arrivée au bout de ce document !
Vous savez maintenant écrire des programmes Python, et charger, préparer, résumer, visualiser et modéliser un jeu de données.
Pour continuer à progresser en analyse de données, la clé est de **pratiquer régulièrement sur de vraies données**. Voici quelques pistes.

* **Analysez des données qui vous intéressent.** Le portail [data.gouv.fr](https://www.data.gouv.fr) rassemble des milliers de jeux de données publics français (élections, transports, santé, environnement…), généralement au format CSV : choisissez-en un qui vous intéresse et posez-lui des questions.
* **Approfondissez la modélisation** avec la [documentation de `statsmodels`](https://www.statsmodels.org/stable/user-guide.html) : modèles linéaires généralisés, modèles mixtes (`mixedlm`), séries temporelles (ARIMA), modèles de survie…
* **Découvrez l'apprentissage automatique** (_machine learning_) avec la bibliothèque [`scikit-learn`](https://scikit-learn.org), dont la documentation contient de nombreux tutoriels : c'est la suite naturelle du projet sur les manchots.
* **Approfondissez `pandas`** grâce à sa [documentation officielle](https://pandas.pydata.org/docs/user_guide/index.html), en particulier les guides sur le regroupement (`groupby`), la restructuration des tableaux (`pivot`, `melt`) et les séries temporelles.
* **Entraînez-vous à programmer** : le site [France-IOI](https://www.france-ioi.org) propose des centaines d'exercices de programmation corrigés automatiquement, classés par niveau, et le [tutoriel officiel de Python](https://docs.python.org/fr/3/tutorial/index.html), en français, approfondit de nombreux points abordés ici.

```{admonition} Un dernier conseil
:class: tip

Quand vous êtes bloquée, pensez à la démarche du chapitre 8 : lire le message d'erreur, observer ce que fait réellement le programme (en affichant `head()`, `shape`, `dtypes`… pour un `DataFrame`), comparer avec ce que vous attendiez.
Et n'oubliez pas que les meilleurs analystes passent, eux aussi, une bonne partie de leur temps à chercher des _bugs_ et à nettoyer des données !
```

Ce document se veut évolutif.
N'hésitez donc pas à faire vos remarques à son auteur, dont vous trouverez le contact sur [sa page web](https://rtavenar.github.io/).
