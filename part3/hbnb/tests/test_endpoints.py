#!/usr/bin/python3
"""
Tests complets pour tous les endpoints HBnB API
Couvre tous les cas positifs et négatifs pour :
- Users, Amenities, Places, Reviews
"""
import unittest
import uuid
from app import create_app
from app.services import facade
from app.persistence.repository import InMemoryRepository


def unique_email():
    """
    Génère un email unique pour chaque test
    """
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def reset_facade():
    """
    Remet les repos du facade à zéro entre les tests
    """
    facade.user_repo = InMemoryRepository()
    facade.place_repo = InMemoryRepository()
    facade.review_repo = InMemoryRepository()
    facade.amenity_repo = InMemoryRepository()


class TestUserEndpoints(unittest.TestCase):
    """
    Tests pour les endpoints /api/v1/users/
    """

    def setUp(self):
        reset_facade()
        self.app = create_app()
        self.client = self.app.test_client()


    # POST /api/v1/users/


    def test_01_create_user_valid(self):
        """
        Création d'un utilisateur valide -> 201
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email()
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')

    def test_02_create_user_duplicate_email(self):
        """
        Email déjà enregistré -> 400
        """
        email = unique_email()
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": email
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_03_create_user_invalid_email_format(self):
        """
        Email invalide -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_03b_create_user_invalid_email_no_domain(self):
        """
        Email sans domaine (test@) -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@"
        })
        self.assertEqual(response.status_code, 400)

    def test_03c_create_user_invalid_email_no_name(self):
        """
        Email sans nom (@example.com) -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_03d_create_user_invalid_email_no_extension(self):
        """
        Email sans extension (test@test) -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@test"
        })
        self.assertEqual(response.status_code, 400)

    def test_03e_create_user_invalid_email_spaces(self):
        """
        Email avec espaces -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "test @example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_03f_create_user_invalid_email_double_at(self):
        """
        Email avec double @ -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@@example.com"
        })
        self.assertEqual(response.status_code, 400)


    def test_04_create_user_empty_first_name(self):
        """
        Prénom vide -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": unique_email()
        })
        self.assertEqual(response.status_code, 400)

    def test_05_create_user_empty_last_name(self):
        """
        Nom de famille vide -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "",
            "email": unique_email()
        })
        self.assertEqual(response.status_code, 400)

    def test_06_create_user_missing_fields(self):
        """
        Champs manquants -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John"
        })
        self.assertEqual(response.status_code, 400)

    def test_07_create_user_first_name_too_long(self):
        """
        Prénom > 50 caractères -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "J" * 51,
            "last_name": "Doe",
            "email": unique_email()
        })
        self.assertEqual(response.status_code, 400)

    def test_08_create_user_last_name_too_long(self):
        """
        Nom > 50 caractères -> 400
        """
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "D" * 51,
            "email": unique_email()
        })
        self.assertEqual(response.status_code, 400)


    # GET /api/v1/users/


    def test_09_get_all_users_empty(self):
        """
        Liste vide au départ -> 200 avec []
        """
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_10_get_all_users_after_creation(self):
        """
        Liste non vide après création -> 200
        """
        self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Martin",
            "email": unique_email()
        })
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

    # GET /api/v1/users/<user_id>


    def test_11_get_user_by_id_valid(self):
        """
        Récupération d'un utilisateur existant -> 200
        """
        post = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Smith",
            "email": unique_email()
        })
        user_id = post.get_json()['id']
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], user_id)

    def test_12_get_user_by_id_not_found(self):
        """
        ID inexistant -> 404
        """
        response = self.client.get('/api/v1/users/nonexistent-id-000')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())


    # PUT /api/v1/users/<user_id>


    def test_13_update_user_valid(self):
        """
        Mise à jour valide -> 200
        """
        post = self.client.post('/api/v1/users/', json={
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": unique_email()
        })
        user_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Charles",
            "last_name": "Brown",
            "email": unique_email()
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['first_name'], 'Charles')

    def test_14_update_user_not_found(self):
        """
        Mise à jour d'un ID inexistant -> 404
        """
        response = self.client.put('/api/v1/users/nonexistent-id-000', json={
            "first_name": "Ghost",
            "last_name": "User",
            "email": unique_email()
        })
        self.assertEqual(response.status_code, 404)

    def test_15_update_user_duplicate_email(self):
        """
        Mise à jour avec email déjà utilisé -> 400
        """
        email1 = unique_email()
        self.client.post('/api/v1/users/', json={
            "first_name": "User1",
            "last_name": "Test",
            "email": email1
        })
        post2 = self.client.post('/api/v1/users/', json={
            "first_name": "User2",
            "last_name": "Test",
            "email": unique_email()
        })
        user2_id = post2.get_json()['id']
        response = self.client.put(f'/api/v1/users/{user2_id}', json={
            "first_name": "User2",
            "last_name": "Test",
            "email": email1
        })
        self.assertEqual(response.status_code, 400)

    def test_16_update_user_invalid_email(self):
        """
        Mise à jour avec email invalide -> 400
        """
        post = self.client.post('/api/v1/users/', json={
            "first_name": "Dave",
            "last_name": "Jones",
            "email": unique_email()
        })
        user_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Dave",
            "last_name": "Jones",
            "email": "not-an-email"
        })
        self.assertEqual(response.status_code, 400)


class TestAmenityEndpoints(unittest.TestCase):
    """
    Tests pour les endpoints /api/v1/amenities/
    """

    def setUp(self):
        reset_facade()
        self.app = create_app()
        self.client = self.app.test_client()


    # POST /api/v1/amenities/


    def test_01_create_amenity_valid(self):
        """
        Création d'une amenity valide -> 201
        """
        response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Wi-Fi')

    def test_02_create_amenity_empty_name(self):
        """
        Nom vide -> 400
        """
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_03_create_amenity_name_too_long(self):
        """
        Nom > 50 caractères -> 400
        """
        response = self.client.post('/api/v1/amenities/', json={"name": "A" * 51})
        self.assertEqual(response.status_code, 400)

    def test_04_create_amenity_missing_name(self):
        """
        Champ name manquant -> 400
        """
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)

    def test_05_create_amenity_name_exactly_50(self):
        """
        Nom exactement 50 caractères -> 201
        """
        response = self.client.post('/api/v1/amenities/', json={"name": "A" * 50})
        self.assertEqual(response.status_code, 201)


    # GET /api/v1/amenities/
 

    def test_06_get_all_amenities(self):
        """
        Liste des amenities -> 200
        """
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_07_get_all_amenities_after_creation(self):
        """
        Liste non vide après création -> 200
        """
        self.client.post('/api/v1/amenities/', json={"name": "Parking"})
        response = self.client.get('/api/v1/amenities/')
        self.assertGreater(len(response.get_json()), 0)


    # GET /api/v1/amenities/<amenity_id>


    def test_08_get_amenity_by_id_valid(self):
        """
        Récupération d'une amenity existante -> 200
        """
        post = self.client.post('/api/v1/amenities/', json={"name": "Pool"})
        amenity_id = post.get_json()['id']
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Pool')

    def test_09_get_amenity_by_id_not_found(self):
        """
        ID inexistant -> 404
        """
        response = self.client.get('/api/v1/amenities/nonexistent-id-000')
        self.assertEqual(response.status_code, 404)


    # PUT /api/v1/amenities/<amenity_id>


    def test_10_update_amenity_valid(self):
        """
        Mise à jour valide -> 200
        """
        post = self.client.post('/api/v1/amenities/', json={"name": "TV"})
        amenity_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Smart TV"})
        self.assertEqual(response.status_code, 200)

    def test_11_update_amenity_not_found(self):
        """
        Mise à jour d'un ID inexistant -> 404
        """
        response = self.client.put('/api/v1/amenities/nonexistent-id-000', json={"name": "Ghost"})
        self.assertEqual(response.status_code, 404)

    def test_12_update_amenity_empty_name(self):
        """
        Mise à jour avec nom vide -> 400
        """
        post = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        amenity_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_13_update_amenity_name_too_long(self):
        """
        Mise à jour avec nom > 50 caractères -> 400
        """
        post = self.client.post('/api/v1/amenities/', json={"name": "Spa"})
        amenity_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "A" * 51})
        self.assertEqual(response.status_code, 400)


class TestPlaceEndpoints(unittest.TestCase):
    """
    Tests pour les endpoints /api/v1/places/
    """

    def setUp(self):
        reset_facade()
        self.app = create_app()
        self.client = self.app.test_client()
        post = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": unique_email()
        })
        self.owner_id = post.get_json()['id']
        post_a = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.amenity_id = post_a.get_json()['id']

    def _valid_place(self, **kwargs):
        data = {
            "title": "Cozy Apartment",
            "description": "Nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        }
        data.update(kwargs)
        return data

    # POST /api/v1/places/


    def test_01_create_place_valid(self):
        """
        Création d'un place valide -> 201
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place())
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Cozy Apartment')

    def test_02_create_place_with_amenities(self):
        """
        Création avec amenities -> 201
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(
            amenities=[self.amenity_id]
        ))
        self.assertEqual(response.status_code, 201)

    def test_03_create_place_invalid_owner(self):
        """
        Owner inexistant -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(
            owner_id="nonexistent-owner-id"
        ))
        self.assertEqual(response.status_code, 400)

    def test_04_create_place_negative_price(self):
        """
        Prix négatif -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(price=-10.0))
        self.assertEqual(response.status_code, 400)

    def test_05_create_place_zero_price(self):
        """
        Prix = 0 -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(price=0))
        self.assertEqual(response.status_code, 400)

    def test_06_create_place_latitude_too_high(self):
        """
        Latitude > 90 -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(latitude=91.0))
        self.assertEqual(response.status_code, 400)

    def test_07_create_place_latitude_too_low(self):
        """
        Latitude < -90 -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(latitude=-91.0))
        self.assertEqual(response.status_code, 400)

    def test_08_create_place_longitude_too_high(self):
        """
        Longitude > 180 -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(longitude=181.0))
        self.assertEqual(response.status_code, 400)

    def test_09_create_place_longitude_too_low(self):
        """
        Longitude < -180 -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(longitude=-181.0))
        self.assertEqual(response.status_code, 400)

    def test_10_create_place_latitude_boundary_max(self):
        """
        Latitude = 90 (limite max) -> 201
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(latitude=90.0))
        self.assertEqual(response.status_code, 201)

    def test_11_create_place_latitude_boundary_min(self):
        """
        Latitude = -90 (limite min) -> 201
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(latitude=-90.0))
        self.assertEqual(response.status_code, 201)

    def test_12_create_place_longitude_boundary_max(self):
        """
        Longitude = 180 (limite max) -> 201
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(longitude=180.0))
        self.assertEqual(response.status_code, 201)

    def test_13_create_place_longitude_boundary_min(self):
        """
        Longitude = -180 (limite min) -> 201
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(longitude=-180.0))
        self.assertEqual(response.status_code, 201)

    def test_14_create_place_empty_title(self):
        """
        Titre vide -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(title=""))
        self.assertEqual(response.status_code, 400)

    def test_15_create_place_title_too_long(self):
        """
        Titre > 100 caractères -> 400
        """
        response = self.client.post('/api/v1/places/', json=self._valid_place(title="T" * 101))
        self.assertEqual(response.status_code, 400)

    def test_16_create_place_missing_required_fields(self):
        """
        Champs requis manquants -> 400
        """
        response = self.client.post('/api/v1/places/', json={"title": "Incomplete"})
        self.assertEqual(response.status_code, 400)


    # GET /api/v1/places/


    def test_17_get_all_places(self):
        """
        Liste des places -> 200
        """
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_18_get_all_places_after_creation(self):
        """
        Liste non vide après création -> 200
        """
        self.client.post('/api/v1/places/', json=self._valid_place())
        response = self.client.get('/api/v1/places/')
        self.assertGreater(len(response.get_json()), 0)


    # GET /api/v1/places/<place_id>


    def test_19_get_place_by_id_valid(self):
        """
        Récupération d'un place existant avec owner et amenities -> 200
        """
        post = self.client.post('/api/v1/places/', json=self._valid_place(
            amenities=[self.amenity_id]
        ))
        place_id = post.get_json()['id']
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('owner', data)
        self.assertIn('amenities', data)
        self.assertEqual(data['owner']['id'], self.owner_id)

    def test_20_get_place_by_id_not_found(self):
        """
        ID inexistant -> 404
        """
        response = self.client.get('/api/v1/places/nonexistent-id-000')
        self.assertEqual(response.status_code, 404)


    # PUT /api/v1/places/<place_id>


    def test_21_update_place_valid(self):
        """
        Mise à jour valide -> 200
        """
        post = self.client.post('/api/v1/places/', json=self._valid_place())
        place_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/places/{place_id}', json=self._valid_place(
            title="Updated Title", price=200.0
        ))
        self.assertEqual(response.status_code, 200)

    def test_22_update_place_not_found(self):
        """
        Mise à jour d'un ID inexistant -> 404
        """
        response = self.client.put('/api/v1/places/nonexistent-id-000',
                                   json=self._valid_place())
        self.assertEqual(response.status_code, 404)

    def test_23_update_place_invalid_price(self):
        """
        Mise à jour avec prix négatif -> 400
        """
        post = self.client.post('/api/v1/places/', json=self._valid_place())
        place_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/places/{place_id}', json=self._valid_place(
            price=-50.0
        ))
        self.assertEqual(response.status_code, 400)

    def test_24_update_place_invalid_latitude(self):
        """
        Mise à jour avec latitude invalide -> 400
        """
        post = self.client.post('/api/v1/places/', json=self._valid_place())
        place_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/places/{place_id}', json=self._valid_place(
            latitude=99.0
        ))
        self.assertEqual(response.status_code, 400)


class TestReviewEndpoints(unittest.TestCase):
    """
    Tests pour les endpoints /api/v1/reviews/
    """

    def setUp(self):
        reset_facade()
        self.app = create_app()
        self.client = self.app.test_client()
        post_u = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "Test",
            "email": unique_email()
        })
        self.user_id = post_u.get_json()['id']
        post_p = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place",
            "price": 80.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.place_id = post_p.get_json()['id']

    def _valid_review(self, **kwargs):
        data = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        data.update(kwargs)
        return data


    # POST /api/v1/reviews/


    def test_01_create_review_valid(self):
        """Création d'une review valide -> 201"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review())
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['text'], 'Great place to stay!')

    def test_02_create_review_rating_1(self):
        """Rating minimum (1) -> 201"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(rating=1))
        self.assertEqual(response.status_code, 201)

    def test_03_create_review_rating_5(self):
        """Rating maximum (5) -> 201"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(rating=5))
        self.assertEqual(response.status_code, 201)

    def test_04_create_review_rating_too_high(self):
        """Rating > 5 -> 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(rating=6))
        self.assertEqual(response.status_code, 400)

    def test_05_create_review_rating_too_low(self):
        """Rating < 1 -> 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(rating=0))
        self.assertEqual(response.status_code, 400)

    def test_06_create_review_rating_negative(self):
        """Rating négatif -> 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(rating=-1))
        self.assertEqual(response.status_code, 400)

    def test_07_create_review_empty_text(self):
        """Texte vide -> 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(text=""))
        self.assertEqual(response.status_code, 400)

    def test_08_create_review_invalid_user(self):
        """User inexistant -> 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(
            user_id="nonexistent-user-id"
        ))
        self.assertEqual(response.status_code, 400)

    def test_09_create_review_invalid_place(self):
        """Place inexistant -> 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(
            place_id="nonexistent-place-id"
        ))
        self.assertEqual(response.status_code, 400)

    def test_10_create_review_missing_fields(self):
        """Champs manquants -> 400"""
        response = self.client.post('/api/v1/reviews/', json={"text": "Nice"})
        self.assertEqual(response.status_code, 400)


    # GET /api/v1/reviews/


    def test_11_get_all_reviews(self):
        """Liste des reviews -> 200"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_12_get_all_reviews_after_creation(self):
        """Liste non vide après création -> 200"""
        self.client.post('/api/v1/reviews/', json=self._valid_review())
        response = self.client.get('/api/v1/reviews/')
        self.assertGreater(len(response.get_json()), 0)


    # GET /api/v1/reviews/<review_id>


    def test_13_get_review_by_id_valid(self):
        """Récupération d'une review existante -> 200"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()['id']
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], review_id)
        self.assertIn('user_id', data)
        self.assertIn('place_id', data)

    def test_14_get_review_by_id_not_found(self):
        """ID inexistant -> 404"""
        response = self.client.get('/api/v1/reviews/nonexistent-id-000')
        self.assertEqual(response.status_code, 404)


    # GET /api/v1/places/<place_id>/reviews


    def test_15_get_reviews_by_place_valid(self):
        """Reviews d'un place existant -> 200 avec reviews"""
        self.client.post('/api/v1/reviews/', json=self._valid_review())
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_16_get_reviews_by_place_not_found(self):
        """Place inexistant -> 404"""
        response = self.client.get('/api/v1/places/nonexistent-id-000/reviews')
        self.assertEqual(response.status_code, 404)

    def test_17_get_reviews_by_place_empty(self):
        """Place sans reviews -> 200 avec []"""
        post_u = self.client.post('/api/v1/users/', json={
            "first_name": "Empty",
            "last_name": "Owner",
            "email": unique_email()
        })
        owner_id = post_u.get_json()['id']
        post_p = self.client.post('/api/v1/places/', json={
            "title": "Empty Place",
            "description": "",
            "price": 50.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": owner_id,
            "amenities": []
        })
        place_id = post_p.get_json()['id']
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    
    # PUT /api/v1/reviews/<review_id>
    

    def test_18_update_review_valid(self):
        """Mise à jour valide -> 200"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=self._valid_review(
            text="Updated review!", rating=4
        ))
        self.assertEqual(response.status_code, 200)

    def test_19_update_review_not_found(self):
        """Mise à jour d'un ID inexistant -> 404"""
        response = self.client.put('/api/v1/reviews/nonexistent-id-000',
                                   json=self._valid_review())
        self.assertEqual(response.status_code, 404)

    def test_20_update_review_invalid_rating(self):
        """Mise à jour avec rating invalide -> 400"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=self._valid_review(
            rating=10
        ))
        self.assertEqual(response.status_code, 400)

    def test_21_update_review_empty_text(self):
        """Mise à jour avec texte vide -> 400"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=self._valid_review(
            text=""
        ))
        self.assertEqual(response.status_code, 400)


    # DELETE /api/v1/reviews/<review_id>


    def test_22_delete_review_valid(self):
        """Suppression d'une review existante -> 200"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()['id']
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

    def test_23_delete_review_not_found(self):
        """Suppression d'un ID inexistant -> 404"""
        response = self.client.delete('/api/v1/reviews/nonexistent-id-000')
        self.assertEqual(response.status_code, 404)

    def test_24_delete_review_then_get(self):
        """Après suppression, GET retourne 404"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()['id']
        self.client.delete(f'/api/v1/reviews/{review_id}')
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)
