# HBnB — Part 4 : front end

Interface web front-end pour l'application HBnB, connectée au back-end Flask

---

## Structure des fichiers

```
part4/
├── index.html        # Liste des logements disponibles
├── login.html        # Formulaire de connexion
├── place.html        # Détail d'un logement + reviews inline
├── add_review.html   # Formulaire d'ajout de review (page dédiée)
├── scripts.js        # Logique JS (Fetch API, auth, DOM)
├── styles.css        # Styles globaux (thème sombre Slate/Teal)
└── images/
    ├── logo.png
    ├── icon.png
    ├── icon_bath.png
    ├── icon_bed.png
    └── icon_wifi.png
```

---

## Prérequis

- Le back-end Part 3 doit tourner sur `http://localhost:5000`
- **CORS activé** sur le back-end Flask (voir section ci-dessous)
- Un navigateur moderne (Chrome, Firefox, Edge)
- Aucune installation front-end requise — fichiers statiques purs

---

## Lancer le projet

###  Démarrer le back-end (Part 3)

```bash
cd ../part3/hbnb
pip install -r requirements.txt
python run.py
# → API disponible sur http://localhost:5000/api/v1
```

###  Ouvrir le front-end

Ouvrir `index.html` directement dans le navigateur **ou** utiliser un serveur local pour éviter les problèmes de cookies :

```bash
# Avec Python
cd part4/
python -m http.server 8080
# → http://localhost:8080
```

>  L'ouverture directe en `file://` peut bloquer les cookies et les requêtes Fetch selon le navigateur. Préférer un serveur local.

---

##  Configurer CORS sur le back-end Flask

Sans cette étape, toutes les requêtes Fetch depuis le front échoueront avec une erreur CORS.

```bash
pip install flask-cors
```

Dans `app/__init__.py` ou `run.py` :

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
```

Pour le développement, autoriser toutes origines :

```python
CORS(app)
```

---

##  Authentification

L'application utilise **JWT (JSON Web Token)** stocké dans un cookie de session.

| Action | Comportement |
|---|---|
| Login réussi | Token JWT stocké dans le cookie `token`, redirect vers `index.html` |
| Login échoué | Message d'erreur affiché sous le formulaire |
| Accès `add_review.html` sans token | Redirect automatique vers `index.html` |
| Cookie absent sur `place.html` | Formulaire de review masqué |

### Tester le login

1. Ouvrir `http://localhost:8080/login.html`
2. Entrer un email/mot de passe valide (créé via l'API en Part 3)
3. Après connexion, vérifier le cookie dans les DevTools → **Application → Cookies** → chercher `token`

Pour créer un utilisateur de test via l'API :

```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@test.com","password":"secret"}'
```

---

## Pages et fonctionnalités

### `index.html` — Liste des logements

- Affiche tous les logements récupérés depuis `GET /api/v1/places/`
- Filtre côté client par prix maximum (10 / 50 / 100 / All)
- Lien **Login** visible si non authentifié, masqué si connecté
- Chaque carte affiche : nom, prix par nuit, bouton "View Details"

### `login.html` — Connexion

- Formulaire email + mot de passe
- Requête `POST /api/v1/auth/login`
- Redirect automatique vers `index.html` si déjà connecté
- Bouton désactivé pendant la requête (anti double-clic)

### `place.html` — Détail d'un logement

- Récupère les détails via `GET /api/v1/places/:id`
- Affiche : hôte, prix, description, équipements
- Récupère et affiche les reviews via `GET /api/v1/places/:id/reviews`
- Si connecté : formulaire inline pour soumettre une review directement
- Si non connecté : section review masquée
- Redirect vers `index.html` si aucun `?id=` dans l'URL

### `add_review.html` — Ajouter une review (page dédiée)

- Accessible uniquement si connecté (sinon redirect `index.html`)
- Récupère le nom du logement via l'API pour l'afficher dans le titre
- Envoi via `POST /api/v1/reviews/`
- Message de succès puis redirect automatique vers `place.html?id=...`
- Lien "Back to place" pour revenir sans soumettre

---

## 🧪 Tests manuels

### Login

```
 Login avec credentials valides → redirect index + cookie créé
 Login avec mauvais mot de passe → message d'erreur rouge
 Login avec serveur éteint → "Cannot reach the server..."
 Double-clic submit → un seul appel API (bouton disabled)
 Accès login.html déjà connecté → redirect index automatique
```

### Index

```
 Sans cookie → lien Login visible, places chargées
 Avec cookie → lien Login masqué, places chargées
 Filtre $10 → seules les places ≤ $10 visibles
 Filtre All → toutes les places visibles
 API inaccessible → message d'erreur dans la liste
 Aucune place → "No places match your filter."
```

### Place Details

```
 URL sans ?id= → redirect index
 ID invalide → "Place not found"
 Connecté → section review affichée
 Non connecté → section review masquée
 Soumission review vide → "Please write your review."
 Soumission valide → succès + rechargement des reviews
```

### Add Review

```
 Accès sans cookie → redirect index immédiat
 URL sans ?id= → redirect index
 Soumission vide → message d'erreur
 Soumission valide → "Review submitted! Redirecting…" + redirect
 Lien "Back to place" → retour vers place.html?id=...
```

---

## Corrections apportées (vs version initiale)

- **`initLogin()`** : ajout d'un `return` après `window.location.href` pour stopper l'exécution si déjà connecté
- **Cookie** : ajout de `SameSite=Lax` pour la protection CSRF
- **Filtre prix** : options générées dynamiquement en JavaScript
- **Titres de page** : mis à jour dynamiquement avec le nom du lieu

---

## Notes techniques

- **Pas de framework** : HTML5, CSS3, JavaScript ES6 natifs uniquement
- **Fetch API** avec `async/await` pour toutes les requêtes
- **XSS** : toutes les données venant de l'API sont passées par `escapeHtml()` avant insertion DOM
- **JWT** : le token est stocké en cookie (pas en `localStorage`) pour une meilleure compatibilité
- **`user_id`** : extrait du payload JWT côté client via `atob()` — en production, le back-end devrait l'extraire lui-même du token

---