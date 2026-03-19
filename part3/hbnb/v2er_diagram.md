# HBnB - Diagrammes Entité-Relation

## Diagramme Principal
```mermaid
erDiagram
    USER {
        char(36) id PK
        varchar(50) first_name
        varchar(50) last_name
        varchar(255) email
        varchar(255) password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    PLACE {
        char(36) id PK
        varchar(100) title
        varchar(255) description
        float price
        float latitude
        float longitude
        char(36) owner_id FK
        datetime created_at
        datetime updated_at
    }

    REVIEW {
        char(36) id PK
        varchar(1024) text
        int rating
        char(36) user_id FK
        char(36) place_id FK
        datetime created_at
        datetime updated_at
    }

    AMENITY {
        char(36) id PK
        varchar(255) name
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        char(36) place_id FK
        char(36) amenity_id FK
    }

    USER ||--o{ PLACE : "possède"
    USER ||--o{ REVIEW : "rédige"
    PLACE ||--o{ REVIEW : "reçoit"
    PLACE ||--o{ PLACE_AMENITY : "possède"
    AMENITY ||--o{ PLACE_AMENITY : "appartient à"
```

### Résumé des Relations

| Entité A | Entité B | Type | Description |
|----------|----------|------|-------------|
| USER | PLACE | 1:N | Un utilisateur peut posséder plusieurs logements. Chaque logement appartient à un seul propriétaire (`owner_id` FK). |
| USER | REVIEW | 1:N | Un utilisateur peut rédiger plusieurs avis. Chaque avis est rédigé par un seul utilisateur (`user_id` FK). |
| PLACE | REVIEW | 1:N | Un logement peut recevoir plusieurs avis. Chaque avis concerne un seul logement (`place_id` FK). |
| PLACE | AMENITY | N:N | Un logement peut avoir plusieurs équipements et un équipement peut appartenir à plusieurs logements. Relation gérée via la table `PLACE_AMENITY`. |
| USER + PLACE | REVIEW | UNIQUE | Un utilisateur ne peut laisser qu'un seul avis par logement (contrainte UNIQUE sur `user_id` + `place_id`). |

---

## Diagramme Étendu — Avec Réservation
```mermaid
erDiagram
    USER {
        char(36) id PK
        varchar(50) first_name
        varchar(50) last_name
        varchar(255) email
        varchar(255) password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    PLACE {
        char(36) id PK
        varchar(100) title
        varchar(255) description
        float price
        float latitude
        float longitude
        char(36) owner_id FK
        datetime created_at
        datetime updated_at
    }

    REVIEW {
        char(36) id PK
        varchar(1024) text
        int rating
        char(36) user_id FK
        char(36) place_id FK
        datetime created_at
        datetime updated_at
    }

    AMENITY {
        char(36) id PK
        varchar(255) name
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        char(36) place_id FK
        char(36) amenity_id FK
    }

    RESERVATION {
        char(36) id PK
        char(36) user_id FK
        char(36) place_id FK
        datetime start_date
        datetime end_date
        float total_price
        varchar(50) status
        datetime created_at
        datetime updated_at
    }

    USER ||--o{ PLACE : "possède"
    USER ||--o{ REVIEW : "rédige"
    PLACE ||--o{ REVIEW : "reçoit"
    PLACE ||--o{ PLACE_AMENITY : "possède"
    AMENITY ||--o{ PLACE_AMENITY : "appartient à"
    USER ||--o{ RESERVATION : "effectue"
    PLACE ||--o{ RESERVATION : "fait l'objet de"
```

### Résumé des Relations

| Entité A | Entité B | Type | Description |
|----------|----------|------|-------------|
| USER | PLACE | 1:N | Un utilisateur peut posséder plusieurs logements. Chaque logement appartient à un seul propriétaire (`owner_id` FK). |
| USER | REVIEW | 1:N | Un utilisateur peut rédiger plusieurs avis. Chaque avis est rédigé par un seul utilisateur (`user_id` FK). |
| PLACE | REVIEW | 1:N | Un logement peut recevoir plusieurs avis. Chaque avis concerne un seul logement (`place_id` FK). |
| PLACE | AMENITY | N:N | Un logement peut avoir plusieurs équipements et un équipement peut appartenir à plusieurs logements. Relation gérée via la table `PLACE_AMENITY`. |
| USER + PLACE | REVIEW | UNIQUE | Un utilisateur ne peut laisser qu'un seul avis par logement (contrainte UNIQUE sur `user_id` + `place_id`). |
| USER | RESERVATION | 1:N | Un utilisateur peut effectuer plusieurs réservations. Chaque réservation est liée à un seul utilisateur (`user_id` FK). |
| PLACE | RESERVATION | 1:N | Un logement peut faire l'objet de plusieurs réservations. Chaque réservation concerne un seul logement (`place_id` FK). |