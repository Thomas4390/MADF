# Méthodes d'apprentissages appliquées aux données financières

## Objectifs : 


Créer une stratégie d’investissement réaliste basée sur les techniques d’apprentissage vues dans le cours. Vous êtes libres de choisir le type de stratégies entre stock picking, market timing, geography/sector rotation, currency trading, crypto trading, ou autre stratégie.

## Ce qu’on vous demande : 


1.	Les données doivent être différentes de celles que nous avons utilisées en classe. 
2.	Il faut au moins avoir 50 séries de données 
3.	Le backtest doit se faire sur une fenêtre de 5 ans à une fréquence mensuelle. 
4.	Très important d’expliquer les choix des stratégies et les choix des techniques d’apprentissage retenues et les techniques délaissées. 
5.	Les techniques d’apprentissage doivent au moins inclure une régression et une technique de classification. 
6.	Très important de faire, lorsque possible, le lien entre la performance de la stratégie et les fondamentaux ou l’intuition financière. 
7.	Justifiez pourquoi la/(les) stratégies doivent (ou pas) être retenue en comparaison avec une approche de gestions passive. 


## Vos livrables :


### 1 - Un rapport (50 points)  

Vous devez fournir un rapport professionnel de 10 pages (max) qui explique : 
- La (ou les) stratégie retenue, 
- Une description détaillée de la construction de la stratégie et l’utilisation des techniques d’apprentissage. (On peut donner les détails mathématiques.) 
- Présenter les faiblesses et les forces de l’approche. 
- Présenter la performance de la stratégie et expliquer, lorsque possible, le lien entre la performance de la stratégie et l’intuition financière. 
- Donnez les arguments pour recommander ou pas la stratégie (rendement-risque). 


### 2 - Un code R, Python ou Matlab (50 points)  


Vous devez fournir un fichier zip qui contient votre code. Le code doit être structuré de la manière suivante : (l’extension .R est pour le code R, vous avez les équivalents dans les autres logiciels)


- run_install_packages.R	file to install all required packages.
- run_strategy.R	file to run the backtest
- data folder	with the raw data and a README file explaining from where they have been taken (with the steps)
- run_data.R	file to process the raw data if necessary or retrieve the data from the web.
- functions folder outputs folder	with R files containing your functions
- outputs folder 	with all the tables and plots generated from run_strategy.R.
- L’évaluation du code tiendra compte de la structure du projet, de la convention de code, de l’efficacité et de la justesse.
