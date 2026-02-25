HBnB Evolution - Partie 2 : Logique Métier et Implémentation de l'API

Présentation du Projet

Cette phase du projet HBnB consiste à implémenter les fonctionnalités de base de l'application en utilisant Python et Flask. L'objectif est de structurer l'application en couches distinctes pour séparer la logique de présentation de la logique métier, garantissant ainsi une base saine et évolutive.

* Le projet permet de gérer les Utilisateurs (Users), les Lieux (Places), les Avis (Reviews) et les Équipements (Amenities).

* Architecture et Logique du Code
Le projet repose sur une Architecture en Couches et l'utilisation du Pattern Façade. Cette approche permet de modifier une partie du code (comme la base de données plus tard) sans impacter les autres couches.

* Structure en Couches
Couche de Présentation (API) : Située dans app/api/v1/. Elle définit les routes (endpoints) et gère les entrées/sorties JSON via flask-restx.

Couche de Logique Métier : Située dans app/models/. Elle contient les règles de gestion et les entités.

Couche de Persistance : Gère le stockage des données (actuellement en mémoire via un système de Repository)
* Le Modèle "Façade"
La Facade sert d'interface unique entre l'API et la logique métier. L'API ne communique jamais directement avec les modèles ou le stockage. Elle demande à la Façade, qui se charge de coordonner les actions entre les différentes entités.

* Relations et Interactions
Voici comment les entités interagissent entre elles au sein de la logique métier :

Plaintext
  [ User ] <------- (Propriétaire) ------- [ Place ]
     |                                       |
     |                                       |
 (Auteur)                                (Cible)
     |                                       |
     v                                       v
  [ Review ] ------------------------------> [ Place ]
                                             |
                                             |
  [ Amenity ] <--- (Plusieurs à Plusieurs) --+

*User / Place : Relation 1:N (Un utilisateur peut posséder plusieurs lieux).

*Place / Amenity : Relation N:N (Un lieu peut avoir plusieurs équipements, et inversement).

*Review : Un avis lie obligatoirement un utilisateur (auteur) et un lieu (cible)

* Concepts Techniques Clés
Sérialisation des données : Conversion des objets complexes en JSON. Nous incluons des attributs étendus  ex: une Place affiche les détails du propriétaire et non un simple ID (payload) 

Opérations CRUD : Implémentation complète des méthodes de création, lecture, mise à jour . Delette non implementer

Validation Métier (Edge Cases) : Auto-validation des modèles (ex: emails valides, limites de caractères, notes entre 1 et 5)

Découplage : Indépendance totale entre l'interface API et le mode de stockage grâce à la Façade

* Installation et Configuration
Cloner le dépôt :

Bash
git clone https://github.com/add1ktion/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2/hbnb
Environnement virtuel et dépendances :

Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Lancer l'application :

Bash
python3 run.py
* Validation et Tests
Nous utilisons des tests unitaires pour valider la logique métier et les réponses de l'API.

Lancer les tests :

Bash
python3 test_T1.py
(Tests actuels : Création d'utilisateurs, lieux, équipements et validation des relations.)

📚 Documentation de l'API
L'API est auto-documentée via Swagger. Une fois le serveur lancé, accédez à la documentation interactive :
http://127.0.0.1:5000/api/v1/

Auteurs :

Batts Antoine (add1ktion)
Laubert alexis (loties1533) 
