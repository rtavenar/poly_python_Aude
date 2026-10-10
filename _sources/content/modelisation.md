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

(ch:modelisation)=
# Modélisation statistique avec `statsmodels`

```{code-cell}
:tags: [remove-cell]
# Réglage d'affichage pour la version PDF (cellule masquée)
import pandas as pd
pd.set_option("display.width", 70)
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
```

```{admonition} Objectifs du chapitre
:class: note

À la fin de ce chapitre, vous saurez :

* ajuster un modèle de régression linéaire avec une **formule** (comme `lm` en R) et lire ses résultats ;
* intégrer des variables qualitatives et des interactions ;
* faire des prédictions et vérifier les résidus ;
* ajuster une régression logistique et interpréter des _odds ratios_ ;
* réaliser les tests classiques (Student, khi-deux, ANOVA) avec `statsmodels` et `scipy.stats`.

**Prérequis :** chapitres 11 à 13, et des connaissances en statistique (régression, tests). **Durée indicative :** 2h.
```

Si vous avez déjà pratiqué la statistique avec R ou SAS, ce chapitre vous montre comment retrouver vos outils habituels en Python.
La bibliothèque `statsmodels` est la plus proche de l'esprit de R et de SAS : elle produit des tableaux de résultats complets (coefficients, erreurs standard, tests, intervalles de confiance…) et permet de décrire les modèles avec des **formules** très proches de celles de R.
Pour les tests statistiques élémentaires, on utilise aussi le module `stats` de la bibliothèque `scipy`.

```{admonition} Installation
:class: tip

`statsmodels` et `scipy` sont inclus dans Anaconda et dans Google Colab. Sinon : `pip install statsmodels scipy`.
```

```{code-cell}
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats

manchots = pd.read_csv("donnees/penguins.csv").dropna()
titanic = pd.read_csv("donnees/titanic.csv")
```

Par convention, on importe l'interface « formules » de `statsmodels` sous le nom `smf`, et l'interface générale sous le nom `sm`.
Nous avons retiré d'emblée les manchots ayant des valeurs manquantes (`dropna()`), pour que tous les modèles portent sur les mêmes 333 individus.

## Correspondances avec R et SAS

| Objectif | R | SAS | Python |
|---|---|---|---|
| Régression linéaire | `lm(y ~ x1 + x2, data = d)` | `PROC REG` / `PROC GLM` | `smf.ols("y ~ x1 + x2", data=d).fit()` |
| Résultats détaillés | `summary(modele)` | (sortie de la procédure) | `modele.summary()` |
| Variable qualitative | `factor(x)` | instruction `CLASS` | `C(x)` dans la formule |
| Régression logistique | `glm(y ~ x, family = binomial)` | `PROC LOGISTIC` | `smf.logit("y ~ x", data=d).fit()` |
| GLM (Poisson…) | `glm(..., family = poisson)` | `PROC GENMOD` | `smf.glm("y ~ x", data=d, family=sm.families.Poisson()).fit()` |
| Table d'ANOVA | `anova(modele)` | `PROC GLM` | `sm.stats.anova_lm(modele, typ=2)` |
| Test de Student | `t.test(x, y)` | `PROC TTEST` | `stats.ttest_ind(x, y)` |
| Test du khi-deux | `chisq.test(table)` | `PROC FREQ` / `CHISQ` | `stats.chi2_contingency(table)` |
| Corrélation | `cor.test(x, y)` | `PROC CORR` | `stats.pearsonr(x, y)` |
| Prédictions | `predict(modele, newdata)` | `OUTPUT OUT= P=` | `modele.predict(nouvelles_donnees)` |

## La régression linéaire

### Un premier modèle

Modélisons la masse d'un manchot en fonction de la longueur de sa nageoire.
La syntaxe est presque celle de R : une formule `"y ~ x"` (sous forme de chaîne de caractères), le `DataFrame` passé en argument `data`, puis la méthode `fit()` qui ajuste le modèle :

```{code-cell}
modele = smf.ols("body_mass_g ~ flipper_length_mm", data=manchots).fit()
print(modele.summary())
```

`ols` signifie _Ordinary Least Squares_ (moindres carrés ordinaires).
Dans un notebook, écrire simplement `modele.summary()` (sans `print`) affiche les mêmes résultats sous forme de tableaux mis en forme.
La sortie de `summary()` ressemble beaucoup à celle de R ou de SAS :

* en haut, les caractéristiques globales : nombre d'observations, $R^2$ (`R-squared`) et $R^2$ ajusté, statistique de Fisher et sa _p_-valeur, critères AIC et BIC ;
* au milieu, le tableau des coefficients : estimation (`coef`), erreur standard, statistique _t_, _p_-valeur (`P>|t|`) et intervalle de confiance à 95 % ;
* en bas, quelques diagnostics sur les résidus (normalité, autocorrélation).

Ici, chaque millimètre de nageoire supplémentaire est associé, en moyenne, à environ 50 g de masse en plus, et le modèle explique 76 % de la variance de la masse.

### Accéder aux résultats

Comme en R (`coef(modele)`, `confint(modele)`…), chaque élément du résultat est accessible séparément, ce qui permet de l'utiliser dans la suite d'un programme :

```{code-cell}
print(modele.params)          # coefficients (une Series)
print(modele.rsquared)        # R²
print(modele.pvalues)         # p-valeurs
print(modele.conf_int())      # intervalles de confiance (un DataFrame)
```

Les attributs `modele.fittedvalues` et `modele.resid` contiennent les valeurs ajustées et les résidus, et `modele.nobs` le nombre d'observations utilisées.

### Variables qualitatives et interactions

Les formules acceptent les mêmes constructions qu'en R :

| Formule | Signification |
|---|---|
| `y ~ x1 + x2` | deux variables explicatives |
| `y ~ C(x)` | `x` traitée comme variable qualitative (codage par indicatrices, la première modalité servant de référence) |
| `y ~ x1 * x2` | effets principaux et interaction (`x1 + x2 + x1:x2`) |
| `y ~ x1:x2` | interaction seule |
| `y ~ np.log(x)` | transformation d'une variable |
| `y ~ I(x ** 2)` | calcul arithmétique dans la formule |
| `y ~ x - 1` | modèle sans constante |

Les colonnes de texte sont automatiquement traitées comme qualitatives, mais il est plus lisible (et indispensable pour une variable codée par des nombres, comme une classe 1, 2, 3) d'écrire `C(...)` :

```{code-cell}
modele2 = smf.ols("body_mass_g ~ flipper_length_mm + C(species) + C(sex)", data=manchots).fit()
print(modele2.summary().tables[1])   # seulement le tableau des coefficients
```

Le coefficient `C(sex)[T.MALE]` s'interprète ainsi : à longueur de nageoire et espèce égales, les mâles pèsent en moyenne 530 g de plus que les femelles (la modalité de référence, `FEMALE`, est la première par ordre alphabétique).
Pour choisir une autre modalité de référence : `C(species, Treatment(reference="Gentoo"))`.

### Prédire

La méthode `predict` calcule les prédictions pour de nouvelles observations, fournies sous la forme d'un `DataFrame` ayant les mêmes noms de colonnes que les données d'origine :

```{code-cell}
nouveaux = pd.DataFrame({
    "flipper_length_mm": [190, 220],
    "species": ["Adelie", "Gentoo"],
    "sex": ["FEMALE", "MALE"]
})
modele2.predict(nouveaux)
```

Pour obtenir aussi les intervalles de confiance et de prédiction : `modele2.get_prediction(nouveaux).summary_frame(alpha=0.05)`.

### Vérifier les hypothèses

Comme en R avec `plot(modele)`, on vérifie l'absence de structure dans les résidus et leur normalité approximative :

```{code-cell}
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
axes[0].scatter(modele2.fittedvalues, modele2.resid, alpha=0.5)
axes[0].axhline(0, color="grey", linestyle="--")
axes[0].set_xlabel("Valeurs ajustées")
axes[0].set_ylabel("Résidus")
axes[0].set_title("Résidus en fonction des valeurs ajustées")
sm.qqplot(modele2.resid, line="s", ax=axes[1])
axes[1].set_title("Diagramme quantile-quantile des résidus")
fig.tight_layout()
plt.show()
```

### Comparer des modèles et tables d'ANOVA

La fonction `sm.stats.anova_lm` produit des tables d'analyse de la variance (avec `typ=2` ou `typ=3` pour les sommes des carrés de type II ou III, comme dans `PROC GLM` ou `car::Anova` en R) :

```{code-cell}
sm.stats.anova_lm(modele2, typ=2)
```

Avec deux modèles emboîtés, elle réalise le test de Fisher de comparaison (comme `anova(m1, m2)` en R) :

```{code-cell}
sm.stats.anova_lm(modele, modele2)
```

Une ANOVA à un facteur n'est rien d'autre qu'une régression sur une variable qualitative :

```{code-cell}
anova_espece = smf.ols("body_mass_g ~ C(species)", data=manchots).fit()
sm.stats.anova_lm(anova_espece, typ=2)
```

```{admonition} Si vous venez de R
:class: seealso

* Ne pas oublier `.fit()` : `smf.ols(...)` seul ne fait que **définir** le modèle.
* Comme `lm` par défaut, `statsmodels` supprime les lignes ayant des valeurs manquantes dans les variables du modèle : vérifiez toujours `modele.nobs`.
* Il existe aussi une interface sans formule, `sm.OLS(y, X)`, plus proche de la notation matricielle ; elle n'ajoute **pas** de constante automatiquement (il faut utiliser `sm.add_constant(X)`). Les formules sont plus simples pour commencer.
* Pour les modèles mixtes (`lme4`), voir `smf.mixedlm` ; pour l'apprentissage automatique (forêts aléatoires, validation croisée…), la bibliothèque de référence est `scikit-learn`.
```

## La régression logistique

Pour une variable à expliquer binaire (0 / 1), on utilise la régression logistique, avec `smf.logit` (ou, de façon équivalente, `smf.glm(..., family=sm.families.Binomial())`).
Modélisons la survie des passagers du Titanic :

```{code-cell}
logit = smf.logit("survived ~ C(sex) + C(pclass) + age", data=titanic).fit()
print(logit.summary())
```

L'argument `disp=0` de `fit()` supprime le message sur la convergence de l'algorithme.
Remarquez le nombre d'observations : 714, car les 177 passagers sans âge ont été écartés.

Les coefficients sont exprimés sur l'échelle du logarithme de la cote (_log-odds_). Pour obtenir les **_odds ratios_**, comme dans la sortie de `PROC LOGISTIC`, on prend leur exponentielle, ainsi que celle des bornes des intervalles de confiance :

```{code-cell}
odds_ratios = pd.DataFrame({
    "OR": np.exp(logit.params),
    "IC 2.5 %": np.exp(logit.conf_int()[0]),
    "IC 97.5 %": np.exp(logit.conf_int()[1]),
}).round(3)
odds_ratios
```

À classe et âge égaux, la cote de survie d'un homme est environ 12 fois plus faible que celle d'une femme (_odds ratio_ de 0,08) ; chaque année d'âge supplémentaire multiplie la cote par 0,96.

La méthode `predict` donne ici des **probabilités** :

```{code-cell}
passagers = pd.DataFrame({"sex": ["female", "male"], "pclass": [1, 3], "age": [30, 30]})
logit.predict(passagers).round(3)
```

## Les tests statistiques classiques

Le module `scipy.stats` fournit les tests usuels. Ils prennent en argument des `Series` (ou des tableaux) et retournent un résultat contenant la statistique et la _p_-valeur.

### Comparer deux moyennes : test de Student

Les mâles Adélie sont-ils plus lourds que les femelles ?

```{code-cell}
adelie = manchots[manchots["species"] == "Adelie"]
males = adelie.loc[adelie["sex"] == "MALE", "body_mass_g"]
femelles = adelie.loc[adelie["sex"] == "FEMALE", "body_mass_g"]

resultat = stats.ttest_ind(males, femelles, equal_var=False)   # test de Welch
print(resultat.statistic, resultat.pvalue)
```

`equal_var=False` correspond au test de Welch (le défaut de `t.test` en R) ; avec `equal_var=True`, on obtient le test de Student classique. Pour des échantillons appariés, on utilise `stats.ttest_rel`, et pour un test non paramétrique, `stats.mannwhitneyu`.

### Indépendance de deux variables qualitatives : test du khi-deux

La survie est-elle indépendante du sexe ?

```{code-cell}
tableau = pd.crosstab(titanic["sex"], titanic["survived"])
khi2, p, ddl, attendus = stats.chi2_contingency(tableau)
print(tableau)
print(f"khi-deux = {khi2:.1f}, ddl = {ddl}, p-valeur = {p:.2e}")
```

`chi2_contingency` retourne quatre valeurs (statistique, _p_-valeur, degrés de liberté et effectifs attendus sous l'hypothèse d'indépendance), que l'on récupère par **déballage**, comme un _tuple_ (chapitre 7).
Remarquez qu'il applique par défaut la correction de continuité de Yates pour les tableaux 2 × 2, comme `chisq.test` en R.

### Corrélation

```{code-cell}
r, p = stats.pearsonr(manchots["flipper_length_mm"], manchots["body_mass_g"])
print(f"r = {r:.3f}, p-valeur = {p:.2e}")
```

`stats.spearmanr` calcule la corrélation des rangs de Spearman.

```{admonition} Testez-vous
:class: hint

1. Quelle formule `statsmodels` correspond au modèle R `lm(y ~ factor(groupe) + age, data = d)` ?
2. Que se passe-t-il si l'on écrit `modele = smf.ols("y ~ x", data=d)` puis `modele.params` ?
3. Comment obtenir l'_odds ratio_ associé à une variable dans un modèle `logit` ?
```

```{raw} latex
\iffalse
```

```{admonition} Réponse
:class: tip, dropdown

1. `smf.ols("y ~ C(groupe) + age", data=d).fit()`.
2. Une erreur (`AttributeError`) : sans `.fit()`, le modèle est seulement défini, pas ajusté, et n'a donc pas de coefficients.
3. En prenant l'exponentielle du coefficient : `np.exp(modele.params["nom_du_coefficient"])`.
```

```{raw} latex
\fi
```

## Exercices

```{admonition} Rappel
:class: tip

Ces exercices sont à faire dans un notebook, avec `pandas`, `numpy`, `statsmodels.formula.api as smf`, `statsmodels.api as sm` et `scipy.stats` importés.
```

(ex14.1)=
```{admonition} Exercice 14.1 : Le bec des manchots ★
Avec les manchots (sans valeurs manquantes) :

1. ajustez la régression de l'épaisseur du bec (`bill_depth_mm`) sur sa longueur (`bill_length_mm`). Quel est le signe de la pente ?
2. ajoutez l'espèce comme variable explicative. Que devient le signe de la pente ? Comment l'expliquer (pensez au nuage de points coloré par espèce du chapitre 13) ?
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf

manchots = pd.read_csv("donnees/penguins.csv").dropna()

m1 = smf.ols("bill_depth_mm ~ bill_length_mm", data=manchots).fit()
print(m1.params)   # pente négative (environ -0.08)

m2 = smf.ols("bill_depth_mm ~ bill_length_mm + C(species)", data=manchots).fit()
print(m2.params)   # pente positive (environ +0.20)
```

C'est un exemple classique de **paradoxe de Simpson** : au sein de chaque espèce, les becs plus longs sont aussi plus épais (pente positive), mais les Gentoo ont à la fois des becs longs et fins, ce qui inverse la tendance lorsqu'on mélange les espèces.
Le modèle sans l'espèce confond l'effet de la longueur du bec et celui de l'espèce.
````

```{raw} latex
\fi
```

(ex14.2)=
```{admonition} Exercice 14.2 : Interaction ★★
Le lien entre la longueur de la nageoire et la masse est-il le même pour les trois espèces ?
Ajustez un modèle avec interaction entre `flipper_length_mm` et `species`, puis comparez-le au modèle sans interaction avec un test de Fisher.
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm

manchots = pd.read_csv("donnees/penguins.csv").dropna()
sans = smf.ols("body_mass_g ~ flipper_length_mm + C(species)", data=manchots).fit()
avec = smf.ols("body_mass_g ~ flipper_length_mm * C(species)", data=manchots).fit()
print(avec.params)
print(sm.stats.anova_lm(sans, avec))
```

La _p_-valeur du test de comparaison (environ 0,005) indique que les pentes diffèrent un peu selon l'espèce : chez les Gentoo, la masse augmente plus vite avec la longueur de la nageoire.
````

```{raw} latex
\fi
```

(ex14.3)=
```{admonition} Exercice 14.3 : Survie et tarif ★★
1. Ajustez une régression logistique de la survie sur le sexe, la classe et le prix du billet (`fare`). Le prix du billet a-t-il un effet significatif une fois la classe prise en compte ?
2. Remplacez `fare` par `np.log1p(fare)` (le logarithme de 1 + prix, car certains billets valent 0). Que constatez-vous ?
3. Calculez la probabilité de survie prédite par le premier modèle pour un homme de 3e classe ayant payé 8 et pour une femme de 1re classe ayant payé 80.
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

titanic = pd.read_csv("donnees/titanic.csv")

m1 = smf.logit("survived ~ C(sex) + C(pclass) + fare", data=titanic).fit(disp=0)
print(m1.summary().tables[1])   # fare : p-valeur d'environ 0.4, non significatif

m2 = smf.logit("survived ~ C(sex) + C(pclass) + np.log1p(fare)", data=titanic).fit(disp=0)
print(m2.summary().tables[1])   # toujours non significatif

passagers = pd.DataFrame({"sex": ["male", "female"], "pclass": [3, 1], "fare": [8, 80]})
print(m1.predict(passagers).round(3))   # environ 0.10 et 0.91
```

Une fois la classe prise en compte, le prix du billet n'apporte presque plus d'information : prix et classe sont très liés.
````

```{raw} latex
\fi
```

(ex14.4)=
```{admonition} Exercice 14.4 : Tests ★★
1. La longueur moyenne de la nageoire diffère-t-elle entre les manchots Adélie de l'île Dream et ceux de l'île Biscoe ? (Test de Welch.)
2. La survie sur le Titanic est-elle indépendante de la classe ? (Test du khi-deux.)
3. Retrouvez le résultat de la question 2 avec une régression logistique et un test du rapport de vraisemblance (attribut `llr_pvalue` du modèle).
```

```{raw} latex
\iffalse
```

````{admonition} Solution
:class: tip, dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

manchots = pd.read_csv("donnees/penguins.csv").dropna()
titanic = pd.read_csv("donnees/titanic.csv")

adelie = manchots[manchots["species"] == "Adelie"]
dream = adelie.loc[adelie["island"] == "Dream", "flipper_length_mm"]
biscoe = adelie.loc[adelie["island"] == "Biscoe", "flipper_length_mm"]
print(stats.ttest_ind(dream, biscoe, equal_var=False))   # p-valeur d'environ 0.4 : pas de différence mise en évidence

khi2, p, ddl, attendus = stats.chi2_contingency(pd.crosstab(titanic["pclass"], titanic["survived"]))
print(khi2, ddl, p)   # khi-deux d'environ 102,9 à 2 ddl : dépendance très nette

m = smf.logit("survived ~ C(pclass)", data=titanic).fit(disp=0)
print(m.llr, m.llr_pvalue)   # test du rapport de vraisemblance : même conclusion
```
````

```{raw} latex
\fi
```

## Bilan du chapitre

```{admonition} À retenir
:class: important

* `import statsmodels.formula.api as smf` ; `modele = smf.ols("y ~ x1 + C(x2)", data=df).fit()` ; `modele.summary()`.
* Résultats : `params`, `pvalues`, `conf_int()`, `rsquared`, `resid`, `fittedvalues`, `nobs` ; prédictions : `modele.predict(nouveau_df)`.
* Formules : `C(x)` (qualitative), `x1 * x2` (interaction), `np.log(x)`, `I(x ** 2)`.
* ANOVA : `sm.stats.anova_lm(modele, typ=2)` ; comparaison de modèles emboîtés : `sm.stats.anova_lm(m1, m2)`.
* Logistique : `smf.logit("y ~ ...", data=df).fit()` ; _odds ratios_ : `np.exp(modele.params)`.
* Tests : `stats.ttest_ind`, `stats.chi2_contingency`, `stats.pearsonr` (module `scipy.stats`).
```

Faites le point : êtes-vous capable de…

- traduire un modèle `lm` ou `glm` de R (ou une `PROC REG` / `PROC LOGISTIC`) en Python ?
- lire le tableau de résultats d'un modèle et en extraire les coefficients et les _p_-valeurs ?
- inclure une variable qualitative et une interaction dans un modèle ?
- vérifier les résidus d'une régression linéaire ?
- réaliser un test de Student ou du khi-deux ?
