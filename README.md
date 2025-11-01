Suivi du Budget Personnel (Projet Python / Streamlit)

Ce projet est une application web interactive développée en Python à l'aide de la librairie Streamlit. Son objectif principal est de fournir un outil simple et efficace pour l'enregistrement et le suivi en temps réel des revenus et des dépenses personnelles.

Objectif du Projet

L'application vise à simplifier la gestion financière personnelle en offrant une interface utilisateur claire et accessible.
Les objectifs clés sont :
1.	Saisie Facile : Permettre l'ajout rapide de transactions (revenus ou dépenses) avec des catégories prédéfinies.
2.	Visualisation Instantanée : Fournir un tableau de bord (Dashboard) qui met à jour les indicateurs financiers dès qu'une transaction est enregistrée.
3.	Persistance des Données : Assurer que l'historique des transactions est sauvegardé entre les sessions (via le fichier data.csv).
Fonctionnalités Principales
L'application est divisée en plusieurs sections qui travaillent ensemble pour offrir une vue complète de l'état financier.
1. Sécurité et Authentification
•	Mot de Passe (Local) : L'accès à l'application est protégé par un simple mot de passe (PASSWORD = "Hola" dans le code), assurant que seules les personnes autorisées peuvent consulter ou modifier les données.
2. Saisie des Transactions (Barre Latérale)
•	Formulaire de Saisie : Un formulaire clair dans la barre latérale permet d'enregistrer :
o	Le type de transaction (Revenu ou Dépense).
o	La catégorie correspondante (e.g., Alimentation, Salaire, Logement, etc.).
o	La date et le montant.
•	Persistance CSV : Chaque transaction enregistrée est immédiatement ajoutée au DataFrame de la session et sauvegardée dans le fichier local data.csv.
3. Tableau de Bord (Dashboard Résumé)
•	Calculs Clés : Affiche les métriques financières les plus importantes en temps réel :
o	Total des Revenus
o	Total des Dépenses
o	Solde Actuel (Revenus - Dépenses)
•	Visualisation Graphique : Inclut un graphique en barres pour comparer visuellement les totaux des revenus et des dépenses, facilitant la compréhension rapide de la situation budgétaire.
4. Gestion de l'Historique
•	Affichage Détaillé : L'historique complet des transactions est affiché sous forme de tableau (DataFrame) clair, sans les index de Pandas.
•	Suppression : Une fonctionnalité est prévue pour sélectionner et supprimer des transactions spécifiques, permettant ainsi de corriger des erreurs ou de retirer des entrées obsolètes.

