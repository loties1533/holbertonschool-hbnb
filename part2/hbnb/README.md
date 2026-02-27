# HBnB Evolution - Partie 2 : Logique Métier et Implémentation de l'API

## Présentation du Projet

Cette phase du projet HBnB consiste à implémenter les fonctionnalités de base de l'application en utilisant Python et Flask. L'objectif est de structurer l'application en couches distinctes pour séparer la logique de présentation de la logique métier, garantissant ainsi une base saine et évolutive.

Le projet permet de gérer les **Utilisateurs (Users)**, les **Lieux (Places)**, les **Avis (Reviews)** et les **Équipements (Amenities)**.

---

## Architecture et Logique du Code

Le projet repose sur une **Architecture en Couches** et l'utilisation du **Pattern Façade**. Cette approche permet de modifier une partie du code (comme la base de données plus tard) sans impacter les autres couches.

### Structure en Couches

- **Couche de Présentation (API)** : Située dans `app/api/v1/`. Elle définit les routes (endpoints) et gère les entrées/sorties JSON via `flask-restx`.
- **Couche de Logique Métier** : Située dans `app/models/`. Elle contient les règles de gestion et les entités.
- **Couche de Persistance** : Gère le stockage des données (actuellement en mémoire via `InMemoryRepository`).

### Le Modèle "Façade"

La Facade sert d'interface unique entre l'API et la logique métier. L'API ne communique jamais directement avec les modèles ou le stockage. Elle demande à la Façade, qui se charge de coordonner les actions entre les différentes entités.

---

## Structure du Projet

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── amenities.py
│   │       ├── places.py
│   │       └── reviews.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── basemodel.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   └── persistence/
│       ├── __init__.py
│       └── repository.py
├── tests/
│   ├── __init__.py
│   └── test_endpoints.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Relations et Interactions

Voici comment les entités interagissent entre elles au sein de la logique métier :

```
  [ User ] <------- (Propriétaire) ------- [ Place ]
     |                                         |
     |                                         |
 (Auteur)                                  (Cible)
     |                                         |
     v                                         v
  [ Review ] --------------------------------> [ Place ]
                                               |
                                               |
  [ Amenity ] <--- (Plusieurs à Plusieurs) ----+
```

- **User / Place** : Relation 1:N — Un utilisateur peut posséder plusieurs lieux
- **Place / Amenity** : Relation N:N — Un lieu peut avoir plusieurs équipements, et inversement
- **Review** : Un avis lie obligatoirement un utilisateur (`user`) et un lieu (`place`)

---

## Concepts Techniques Clés

- **Sérialisation des données** : Conversion des objets complexes en JSON. Une `Place` affiche les détails du propriétaire et non un simple ID.
- **Opérations CRUD** : Implémentation complète des méthodes de création, lecture, mise à jour. Le DELETE n'est implémenté que pour les Reviews.
- **Validation Métier** : Auto-validation des modèles (emails valides, limites de caractères, notes entre 1 et 5, coordonnées GPS, etc.)
- **Découplage** : Indépendance totale entre l'interface API et le mode de stockage grâce à la Façade.

---

## Installation et Lancement

### Prérequis

- Python 3.10+
- pip3

### Installation des dépendances

```bash
pip3 install flask flask-restx
```

### Lancer le serveur

```bash
cd part2/hbnb
python3 run.py
```

Le serveur démarre sur `http://127.0.0.1:5000`

---

## Documentation de l'API

L'API est auto-documentée via **Swagger**. Une fois le serveur lancé, accédez à la documentation interactive :

```
http://127.0.0.1:5000/api/v1/
```

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/v1/users/` | Créer un utilisateur |
| GET | `/api/v1/users/` | Lister tous les utilisateurs |
| GET | `/api/v1/users/<id>` | Récupérer un utilisateur |
| PUT | `/api/v1/users/<id>` | Modifier un utilisateur |
| POST | `/api/v1/amenities/` | Créer un équipement |
| GET | `/api/v1/amenities/` | Lister tous les équipements |
| GET | `/api/v1/amenities/<id>` | Récupérer un équipement |
| PUT | `/api/v1/amenities/<id>` | Modifier un équipement |
| POST | `/api/v1/places/` | Créer un lieu |
| GET | `/api/v1/places/` | Lister tous les lieux |
| GET | `/api/v1/places/<id>` | Récupérer un lieu avec owner et amenities |
| PUT | `/api/v1/places/<id>` | Modifier un lieu |
| GET | `/api/v1/places/<id>/reviews` | Lister les avis d'un lieu |
| POST | `/api/v1/reviews/` | Créer un avis |
| GET | `/api/v1/reviews/` | Lister tous les avis |
| GET | `/api/v1/reviews/<id>` | Récupérer un avis |
| PUT | `/api/v1/reviews/<id>` | Modifier un avis |
| DELETE | `/api/v1/reviews/<id>` | Supprimer un avis |

---

## Validation et Tests

Les tests unitaires couvrent **toute la chaîne** : API → Facade → Modèle.

### Lancer les tests

```bash
cd part2/hbnb
python3 -m unittest tests/test_endpoints.py -v
```

### Ce qui est testé (77 tests)

| Entité | Tests |
|--------|-------|
| **Users** | Création valide, email dupliqué, formats d'email invalides (sans @, sans domaine, sans extension, avec espaces, double @), noms vides/trop longs, GET liste, GET par ID, PUT update |
| **Amenities** | Création valide, nom vide/trop long, limite exacte 50 chars, GET liste, GET par ID, PUT update |
| **Places** | Création valide, owner invalide, prix négatif/zéro, latitude/longitude hors range et aux limites exactes (±90, ±180), titre vide/trop long, GET liste, GET par ID avec owner et amenities, PUT update |
| **Reviews** | Création valide, rating aux limites (1 et 5), rating invalide (0, 6, -1), texte vide, user/place inexistants, GET par place (vide et non vide), PUT update, DELETE et vérification après suppression |

### Codes de statut testés

- **201** → Création réussie
- **200** → Récupération / mise à jour / suppression réussie
- **400** → Données invalides
- **404** → Ressource inexistante

---

## Lien du Projet

[holbertonschool-hbnb](https://github.com/add1ktion/holbertonschool-hbnb.git)

---

## Auteurs

- **Bats Antoine** (add1ktion) — [GitHub](https://github.com/add1ktion)
- **Laubert Alexis** (loties1533) — [GitHub](https://github.com/loties1533)
