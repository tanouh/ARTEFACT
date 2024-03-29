# MODULE PROJ103: ARTEFACT 2024

## Descriptif du projet 
Il s’agit d’un travail en équipe de 3 à 5 élèves, ayant pour but l'application des connaissances en génie logiciel tout en insistant sur l'aspect collaboratif du projet. 

L'objectif était de pouvoir controler un robot piloté par une carte _RASPBERRY PI_ muni d'une carte de contrôle: _Motor Driver HAT for Raspberry Pi_. 
Les fonctionnalités ont été implémentées majoritairement en Python.

## Développeurs
- Tania Mahandry: @tania.mahandry
- Zhiying Zou: @zhiying.zou
- Alexandre Mallez: @alexandre.mallez

## Fonctionnalités principales
### Conduite manuelle
Contrôle à distance à travers une interface web générée par le serveur de la carte. Réaliser des fonctions telles que avancer, reculer, tourner à gauche et tourner à droite, etc. Capable à effectuer des ajustements de vitesse, via la barre de vitesse sur le site web.

### Conduite autonome 
Etant donné un cahier des charges spécifiques, le robot est capable d'exécuter ses tâches automatiquement : ici, il s'agit d'un parcours suivant la détection de marqueurs Aruco. Il est capable de chercher et rapproche successivement 3 marqueurs Aruco de numéro différents. Après avoir réussi de trouver ces 3 marqueurs, il va rentourner à la zone d'arrive qui est marqué 9.

De plus, ce robot est capable de faire l'exchange des messages avec un serveur central, pour communiquer son état.

## Exécution
Le répertoire de dépôt se trouve dans  : 
`~/repo/teamb/`

Pour lancer le serveur depuis répertoire mentionné ci-dessus :
`python3 ./src/motor/app.py` 

Une fois que le serveur est lancé, les commandes manuelles et l'enclechement du mode autonome se fait sur la page web :  [http://137.194.173.40:5000/](http://137.194.173.40:5000/)
