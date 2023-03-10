# SAE-3.05 - BDBOUM
## SAE Projets 2022-2023 - S3-S4

Cette application à comme objectif la de gestion d'inscription et d'organisation des différents participants pour le festival de bandes dessinées organisé chaque année à Blois par l'association BD Boum. Actuellement, la saisie des données se fait sur le tableur Excel à partir de renseignements donnés sous forme de fiches à l'association par échange de mails ou courrier. L'association retourne ensuite une feuille de route complétée à chaque participant. Afin de simplifier et de moderniser ce processus, l'association souhaite informatiser la saisie et les traitements, ainsi que la feuille de route retournée à chacune des personnes. Ce rapport utilisateur détaillera les différentes fonctionnalités développées dans l'application, afin de répondre aux besoins de l'association BD Boum et de faciliter l'organisation de ce festival de bandes dessinées.

## Table des matières

    Installation
    Requirements libraries
    Contribuer
    Licence

## Installation sur Windows :

Tout d'abord vous devez installer le système de gestion de base de données MySQL. Voici le lien d'une vidéo explicative afin d'installer MySQL sur Windows : 

https://www.youtube.com/watch?v=1oxLmS8MiEo

Vous pouvez vérifier que MySQL est bien installé avec ces étapes : 

Ouvrez l'invite de commande en appuyant sur la touche Windows + R, tapez "cmd" et appuyez sur Entrée.
Dans l'invite de commande, tapez "mysql --version" et appuyez sur Entrée.
Si MySQL est installé, vous devriez voir la version de MySQL installée sur votre machine.

Ensuite vous devez ajouter aux variables d'environnement le programme MySQL afin de pouvoir lancer la base de données ensuite.

Ouvrez l'Explorateur de fichiers Windows.
Cliquez avec le bouton droit de la souris sur "Ce PC" ou "Poste de travail" et sélectionnez "Propriétés".
Cliquez sur "Paramètres système avancés".
Cliquez sur le bouton "Variables d'environnement".
Dans la section "Variables système", recherchez la variable "Path" et cliquez sur "Modifier".
Ajoutez le chemin d'accès au répertoire "bin" de MySQL à la fin de la ligne. Par exemple, si MySQL est installé dans "C:\Program Files\MySQL\MySQL Server 8.0\bin", ajoutez ";C:\Program Files\MySQL\MySQL Server 8.0\bin" (sans les guillemets) à la fin de la ligne existante.
Cliquez sur "OK" pour fermer toutes les fenêtres de paramètres.

Vous devez ensuite initialiser la base de données avec la base de données de bdBOUM : 

Placer vous dans le dossier : \Developpement\scripts\
Ouvrez une invite de commande ou terminale et entrez la commande : mysql -u root -p
Puis initialiser la base de donné avec la commande : source script.sql
Ensuite, inséré des données de tets avec la commande : source insertion.sql

   Normalement, les dernières lignes qui doivent s'afficher dans le terminale MySQL sont : 

          Query OK, 5 rows affected (0,061 sec)
          Records: 5 Duplicates: 0 Warnings: 0

Quitter, puis rendez-vous dans le fichier ConnexionPythonSQL.py qui se trouve dans le dossier : \Developpement\app
 Vérifier que la ligne 88 du fichier soit la seul du paragraphe à être décommenté : 
        connexion ,engine = ouvrir_connexion("root","root","localhost", "BDBOUM")

Maintenant, placez-vous à la racine du projet et ouvrez un terminal puis entrez la commande suivante afin de télécharger toutes les dépendances dont l'application à besoin :
 
python -m pip install -r Developpement\requirement.txt
OU
pip install -r Developpement\requirement.txt

Dès à présent, vous pouvez lancer l'application. Pour cela, soit vous installer Visual Studio Code, et ouvrez le projet avec ce logiciel. Une fois ouvert, dans le bar de navigation à droite rendez-vous dans l'onglet Extensions et installer python. Ensuite cliquez pour afficher le fichier run.py qui se trouve dans le répertoire : \Developpement\run.py puis cliquer sur l’icône triangle en haut à droite nommée "run the Python file" ou "Éxécuter le fichier Python".

Sinon, si vous ne souhaiter pas installer VSCode, vous pouvez ouvrir une invite de commande ou un terminal à la racine du projet et entrer la commande suivante afin de lancer l'application :
python Developpement\run.py

Ensuite quelque soit votre choix effectuer l'étape suivante :
Ouvrez un navigateur puis entrer dans la barre de l'URL : http://127.0.0.1:5000


## Installation sur Linux :

Tout d'abord vous devez installer le système de gestion de base de données MySQL. Voici les étapes à suivre pour installer MySQL sur un OS Linux :

Pour installer MySQL sur Linux, vous pouvez suivre les étapes suivantes :

Ouvrez un terminal sur votre système Linux.
Mettez à jour le gestionnaire de paquets de votre système en exécutant la commande suivante :
Entrez la commande : sudo apt-get update
Installez MySQL en exécutant la commande suivante : sudo apt-get install mysql-server
Suivez les instructions à l'écran pour configurer le mot de passe root pour MySQL.
Une fois l'installation terminée, vérifiez que MySQL est en cours d'exécution en exécutant la commande suivante : sudo service mysql status

Vous devriez voir un message indiquant que MySQL est en cours d'exécution.
Vous pouvez maintenant commencer à utiliser MySQL sur votre système Linux en ouvrant un terminal et en tapant la commande suivante : mysql -u root -p

Vous devez maintenant initialiser la base de données. Pour ceci, entrer la commande : 
source script.sql

Puis pour insérer les données de test, entrer la commande : source insertion.sql
Normalement, les dernières lignes qui doivent s'afficher dans le terminales sont : 

          Query OK, 5 rows affected (0,061 sec)
          Records: 5  Duplicates: 0  Warnings: 0

Dès à présent quitter avec ctrl+z, puis rendez-vous dans le fichier ConnexionPythonSQL.py qui se trouve dans le dossier : \Developpement\app. Ouvrer le avec VSCode ou avec la commande : nano \Developpement\app\ConnexionPythonSQL.py
Vérifier que la ligne 88 du fichier soit la seule du paragraphe à être dé-commenté : 
 connexion ,engine = ouvrir_connexion("root","root","localhost", "BDBOUM")

Maintenant, placez-vous à la racine du projet et ouvrez un terminal puis entrez la commande suivante afin de télécharger toutes les dépendances dont l'application à besoin :
 
python -m pip install -r Developpement\requirement.txt
OU
pip install -r Developpement\requirement.txt

Dès à présent, vous pouvez lancer l'application. Pour cela, soit vous pouvez installer Visual Studio Code, et ouvrir le projet avec ce logiciel. Une fois ouvert, dans le bar de navigation à droite rendez-vous dans l'onglet Extensions et installer python. Ensuite cliquer pour afficher le fichier run.py qui se trouve dans le répertoire : \Developpement\run.py puis cliquer sur l’icône triangulaire en haut à droite nommée "run the Python file" ou "Exécuter le fichier Python".

Sinon, si vous ne souhaiter pas installer VSCode, vous pouvez ouvrir une invite de commande ou un terminal à la racine du projet et entrer la commande suivante afin de lancer l'application :
python Developpement\run.py

Ensuite quelque soit votre choix effectuer l'étape suivante :
Ouvrer un navigateur puis entrer dans la barre de l'URL : http://127.0.0.1:5000

## Requirements libraries

Ces commandes sont des librairies nécessaires au bon fonctionnement de l'application.
Vous devez les installer grâce au fichier requirements.txt, cela est possible avec la 
commande : `pip install -r requirements.txt` OU `python3 -m pip install -r requirement.txt`

install python\
pip install flask\
pip3 install mysql-connector-python\
pip install flask-wtf\
pip install flask-login\
pip install xlsxwriter\
pip install pandas\
pip install sendgrid

## Contribuer

DOUDEAU Luis : Chef de projet\
DE NARDI Lenny : Scrum Master\
CHARPENTIER Maxym

## Licence

GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 

## Link GitHub

https://github.com/luis-doudeau/SAE-3.05-BDBOUM
