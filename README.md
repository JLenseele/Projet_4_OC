<a name="readme-top"></a>
# Chess Tournament

Programme de gestion de tournoi d'échec avec appairage suisse des joueurs

## Features

- Création de nouveau tournoi
- Création de nouveau joueur
- Suivi d'un tournoi de l'ouverture à la cloture
- Affichage de différents rapport

- Sauvegarde des tournois / joueurs dans un .json
- Importation de données depuis un .json

## Requirements

+ [Python v3+](https://www.python.org/downloads/)

## Installation & Get Started

Récuperer le projet sur GitHub

    git clone https://github.com/JLenseele/Projet_4_OC.git
    cd Projet_4_OC

Créer l'environement virtuel

    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt
    
Lancer le Script

    python main.py

## Utilisation

### Global

Aprés lancement, le programme vous permet de créer un nouveau tournoi d'échec, puis d'y inscrire des joueurs.  
Une fois le tournoi plein, il peut alors démarrer.  
Lors du premier tour, la liste des joueurs sera trié en fonction de leur classement (ligue), et les matchs seront créé de la facon suivante :  
[1] -> [5]  
[2] -> [6]  
[3] -> [7]  
[4] -> [8]  
  
Après résolution des matchs, des points sont attribués à chaque joueurs:  
win = +1  
draw = +0.5  
lose = +0  

Pour les rounds suivants, la méthode de pair suisse sera appliqué  
La liste des joueurs sera trié en fonction de leurs score sur le tournoi en cour.  
[1] -> [1]  
[1] -> [0.5]  
[0.5] -> [0]  
[0] -> [0]  

Et ainsi de suite jusqu'a la cloture du tournoi.
Le classement final est affiché.  

### Import / Export

Depuis le menu principal, Il est possible de sauvegarder l'intégralité des tournois/joueurs présent à tous moment.  
Il vous sera alors demander de spécifié un nom de fichier.  
"nom_du_fichier.json sera alors créé dans le dossier root du projet  
(il est tout a fait possible d'enregistrer chaque état du programme dans des fichiers différents, pour conserver les tournois individuellement par exemple)

Il est également possible d'importer ces mêmes fichiers .json a tout moment.  
il faudra cette fois spécifié le nom du fichier déja présent dans le dossier root.  
Le nombre de tournois/joueurs sera alors affiché.  

{bonus} -> un fichier db_saved.json est inclus dans le projet. Il contient un tournoi et 25 joueurs prêt à être utilisé.

### Rapport

Plusieurs rapport sont disponibles depuis le menu principal:  
- liste des joueurs (ordre alph.) / (classements)  
- liste des tournois  
- détails complet d'un tournoi  

## Flake 8

rapport HTML disponible dans ./flake-report/index.html  

config  

    [flake8]
    exclude = git/, env/,  
    max-line-length = 119

## Roadmap

- [x] Création tournois / joueurs
- [x] Gestion d'un tournoi de A à Z
- [x] Génération des rapport
- [x] Import / Export des datas
- [ ] Suppression / Modification des objets (tournois/joueurs)
- [ ] Age minimum des joueurs
- [ ] Interface Graphique

<p align="right">(<a href="#readme-top">back to top</a>)</p>
    
## Reference

+ [Méthode de pair suisse](https://en.wikipedia.org/wiki/Swiss-system_tournament)  

## Contributors

[JLenseele](https://github.com/JLenseele)
