import unittest
import uuid
from app import create_app

class TestHBnBGlobal(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.suffix = uuid.uuid4().hex[:6]

    # --- TESTS : USER & EMAIL ---
    def test_user_cases(self):
        """Test User : Création valide et Erreurs d'email"""
        # Valide
        res = self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe", "email": f"ok_{self.suffix}@test.com"
        })
        self.assertEqual(res.status_code, 201)

        # Invalide : Pas de @
        res_err = self.client.post('/api/v1/users/', json={
            "first_name": "Bad", "last_name": "Mail", "email": "nomail.com"
        })
        self.assertEqual(res_err.status_code, 400)

    # --- TESTS : PLACE & PRIX ---
    def test_place_cases(self):
        """Test Place : Création et Erreur de prix/description"""
        u_res = self.client.post('/api/v1/users/', json={
            "first_name": "Owner", "last_name": "Test", "email": f"owner_{self.suffix}@test.com"
        })
        u_id = u_res.get_json()['id']

        # Valide
        res = self.client.post('/api/v1/places/', json={
            "title": "Nice Place", "description": "Good", "price": 100.0,
            "latitude": 10.0, "longitude": 10.0, "owner_id": u_id
        })
        self.assertEqual(res.status_code, 201)

        # Invalide : Prix négatif
        res_err = self.client.post('/api/v1/places/', json={
            "title": "Free", "description": "D", "price": -5.0, "owner_id": u_id
        })
        self.assertEqual(res_err.status_code, 400)

    # --- TESTS : REVIEW & RATING ---
    def test_review_cases(self):
        """Test Review : Création, Update et Erreur de note"""
        # On a besoin d'un user et d'une place
        u_id = self.client.post('/api/v1/users/', json={"first_name":"A","last_name":"B","email":f"r_{self.suffix}@t.com"}).get_json()['id']
        p_id = self.client.post('/api/v1/places/', json={"title":"T","description":"D","price":10.0,"latitude":0.0,"longitude":0.0,"owner_id":u_id}).get_json()['id']

        # Valide (Create + Get)
        res = self.client.post('/api/v1/reviews/', json={
            "text": "Great", "rating": 5, "user_id": u_id, "place_id": p_id
        })
        self.assertEqual(res.status_code, 201)
        r_id = res.get_json()['id']

        # Invalide : Rating > 5
        res_err = self.client.post('/api/v1/reviews/', json={
            "text": "Too much", "rating": 6, "user_id": u_id, "place_id": p_id
        })
        self.assertEqual(res_err.status_code, 400)

        # Valide (Update)
        res_up = self.client.put(f'/api/v1/reviews/{r_id}', json={"text": "Updated Text"})
        self.assertEqual(res_up.status_code, 200)

    # --- TESTS : AMENITY ---
    def test_amenity_cases(self):
        """Test Amenity : Création et Liste"""
        res = self.client.post('/api/v1/amenities/', json={"name": f"WiFi_{self.suffix}"})
        self.assertEqual(res.status_code, 201)
        
        res_list = self.client.get('/api/v1/amenities/')
        self.assertEqual(res_list.status_code, 200)
        self.assertIsInstance(res_list.get_json(), list)