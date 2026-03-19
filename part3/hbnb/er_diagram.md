# HBnB - Diagrammes Entité-Relation

## Diagramme Principal

```mermaid
erDiagram
    USER {
        char(36)     id         PK
        varchar(50)  first_name
        varchar(50)  last_name
        varchar(255) email
        varchar(255) password
        boolean      is_admin
        datetime     created_at
        datetime     updated_at
    }

    PLACE {
        char(36)     id          PK
        varchar(100) title
        varchar(255) description
        float        price
        float        latitude
        float        longitude
        char(36)     owner_id    FK
        datetime     created_at
        datetime     updated_at
    }

    REVIEW {
        char(36)      id         PK
        varchar(1024) text
        int           rating
        char(36)      user_id    FK
        char(36)      place_id   FK
        datetime      created_at
        datetime      updated_at
    }

    AMENITY {
        char(36)    id         PK
        varchar(50) name
        datetime    created_at
        datetime    updated_at
    }

    PLACE_AMENITY {
        char(36) place_id   FK
        char(36) amenity_id FK
    }

    USER    ||--o{ PLACE         : "possède (owner_id)"
    USER    ||--o{ REVIEW        : "rédige (user_id)"
    PLACE   ||--o{ REVIEW        : "reçoit (place_id)"
    PLACE   ||--|{ PLACE_AMENITY : "référencée dans"
    AMENITY ||--|{ PLACE_AMENITY : "référencée dans"
```

### Résumé des Relations

| Entité A | Entité B     | Type   | Notation   | Clé FK                        | Description                                                                 |
|----------|--------------|--------|------------|-------------------------------|-----------------------------------------------------------------------------|
| USER     | PLACE        | 1:0..N | `\|\|--o{` | `places.owner_id → users.id`  | Un user peut posséder zéro ou plusieurs logements.                          |
| USER     | REVIEW       | 1:0..N | `\|\|--o{` | `reviews.user_id → users.id`  | Un user peut rédiger zéro ou plusieurs avis.                                |
| PLACE    | REVIEW       | 1:0..N | `\|\|--o{` | `reviews.place_id → places.id`| Un logement peut recevoir zéro ou plusieurs avis.                           |
| PLACE    | PLACE_AMENITY| 1:1..N | `\|\|--|{` | `place_amenity.place_id`      | Un logement référencé dans la table d'association a au moins une entrée.    |
| AMENITY  | PLACE_AMENITY| 1:1..N | `\|\|--|{` | `place_amenity.amenity_id`    | Un équipement référencé dans la table d'association a au moins une entrée.  |
| USER + PLACE | REVIEW  | UNIQUE | —          | UNIQUE(user_id, place_id)     | Un user ne peut laisser qu'un seul avis par logement.                       |

---

## Diagramme Étendu — Avec Réservation

```mermaid
erDiagram
    USER {
        char(36)     id         PK
        varchar(50)  first_name
        varchar(50)  last_name
        varchar(255) email
        varchar(255) password
        boolean      is_admin
        datetime     created_at
        datetime     updated_at
    }

    PLACE {
        char(36)     id          PK
        varchar(100) title
        varchar(255) description
        float        price
        float        latitude
        float        longitude
        char(36)     owner_id    FK
        datetime     created_at
        datetime     updated_at
    }

    REVIEW {
        char(36)      id         PK
        varchar(1024) text
        int           rating
        char(36)      user_id    FK
        char(36)      place_id   FK
        datetime      created_at
        datetime      updated_at
    }

    AMENITY {
        char(36)    id         PK
        varchar(50) name
        datetime    created_at
        datetime    updated_at
    }

    PLACE_AMENITY {
        char(36) place_id   FK
        char(36) amenity_id FK
    }

    RESERVATION {
        char(36)    id          PK
        char(36)    user_id     FK
        char(36)    place_id    FK
        datetime    start_date
        datetime    end_date
        float       total_price
        varchar(50) status
        datetime    created_at
        datetime    updated_at
    }

    USER    ||--o{ PLACE        : "possède (owner_id)"
    USER    ||--o{ REVIEW       : "rédige (user_id)"
    PLACE   ||--o{ REVIEW       : "reçoit (place_id)"
    PLACE   ||--|{ PLACE_AMENITY : "référencée dans"
    AMENITY ||--|{ PLACE_AMENITY : "référencée dans"
    USER    ||--o{ RESERVATION  : "effectue (user_id)"
    PLACE   ||--o{ RESERVATION  : "fait l'objet de (place_id)"
```

### Résumé des Relations

| Entité A     | Entité B      | Type   | Notation   | Clé FK                              | Description                                                               |
|--------------|---------------|--------|------------|-------------------------------------|---------------------------------------------------------------------------|
| USER         | PLACE         | 1:0..N | `\|\|--o{` | `places.owner_id → users.id`        | Un user peut posséder zéro ou plusieurs logements.                        |
| USER         | REVIEW        | 1:0..N | `\|\|--o{` | `reviews.user_id → users.id`        | Un user peut rédiger zéro ou plusieurs avis.                              |
| PLACE        | REVIEW        | 1:0..N | `\|\|--o{` | `reviews.place_id → places.id`      | Un logement peut recevoir zéro ou plusieurs avis.                         |
| PLACE        | PLACE_AMENITY | 1:1..N | `\|\|--|{` | `place_amenity.place_id`            | Un logement référencé dans la table d'association a au moins une entrée.  |
| AMENITY      | PLACE_AMENITY | 1:1..N | `\|\|--|{` | `place_amenity.amenity_id`          | Un équipement référencé dans la table d'association a au moins une entrée.|
| USER + PLACE | REVIEW        | UNIQUE | —          | UNIQUE(user_id, place_id)           | Un user ne peut laisser qu'un seul avis par logement.                     |
| USER         | RESERVATION   | 1:0..N | `\|\|--o{` | `reservations.user_id → users.id`   | Un user peut effectuer zéro ou plusieurs réservations.                    |
| PLACE        | RESERVATION   | 1:0..N | `\|\|--o{` | `reservations.place_id → places.id` | Un logement peut faire l'objet de zéro ou plusieurs réservations.         |
