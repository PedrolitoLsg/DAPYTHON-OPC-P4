# *Ce Projet développé en Python fait partie du parcours DA Python dispensé par la plateforme OpenClassroom*
## Projet4 

### Introduction - Projet 4: Chess Club Tournament
Le design pattern utilisé est le MVC, Model View Controller.

Le modèle contient les informations relatives à l’état du système. Ce sont les fonctionnalités brutes de l’application

La vue présente les informations du modèle à l’utilisateur. Elle sert d’interface visuelle pour l’utilisateur.

Le contrôleur garantit que les commandes utilisateurs soient exécutées correctement, modifiant les objets du modèle appropriés, et mettant à jour l’application.C’est finalement les rouages de l’application, et c’est la couche qui apporte une interaction avec l’utilisateur. 

Les librairies utilisées sont flake8-html, Tindydb ainsi que DateTime

### Fonctionnement:
*Le projet a été développé en langue anglaise.*

Pour lancer le script via le terminal, dans le dossier, lancer main.py

Il permet la création et la gestion des données de tournois d'échecs via TinyDb.
###Plusieurs actions utilisateurs sont possibles:
* Création d'un joueur.
* Création d'un tournoi.
* Ajout d'un joueur à un tournoi.
* Création des rounds d'un tournoi.
* Entrée des scores d'un round d'un tournoi.
* Modification du score elo d'un joueur.
* Impression de rapports divers.



### Pré-requis
* Créér un git clone en local afin d'utiliser le script.
* Activer l'environnement virtuel
* Pour connaître les détails de l'environnement nécessaire, voir le document requirements.txt contenant les différentes librairies utilisées pour faire fonctionner ce script.
Sinon dans le terminal entrer:
py -m pip install -r requirements.txt
afin d'installer l'environnement virtuel associé.

* Avant d'utiliser nettoyer le fichier db.json qui contient des joueurs et tournois factices permettant de s'assurer du bon fonctionnement du script.

### Génération du rapport flake8-html
Après avoir installé les différentes librairies
entrer dans le terminal le code:
flake8 --format=html --htmldir=flake-report








