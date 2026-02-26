from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- USER METHODS ---
    def create_user(self, user_data):
        try:
            user = User(**user_data)
            self.user_repo.add(user)
            return user
        except (TypeError, ValueError) as e:
            raise ValueError(f"User creation failed: {e}")

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(data)
        return user

    # --- AMENITY METHODS ---
    def create_amenity(self, amenity_data):
        try:
            amenity = Amenity(**amenity_data)
            self.amenity_repo.add(amenity)
            return amenity
        except (TypeError, ValueError) as e:
            raise ValueError(f"Amenity creation failed: {e}")

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        return amenity

    # --- PLACE METHODS ---
    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("owner_id is required")
            
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.pop('amenities', [])
        place_data['owner'] = owner
        place_data.pop('owner_id', None)

        try:
            place = Place(**place_data)
            
            for a_id in amenity_ids:
                amenity = self.get_amenity(a_id)
                if amenity:
                    place.add_amenity(amenity)

            self.place_repo.add(place)
            return place
        except (TypeError, ValueError) as e:
            raise ValueError(f"Place creation failed: {e}")

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None

        data.pop('owner_id', None)
        place.update(data)
        return place

    # --- REVIEW METHODS ---
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not user_id or not place_id:
            raise ValueError("user_id and place_id are required")

        user = self.get_user(user_id)
        place = self.get_place(place_id)

        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")

        review_data['user'] = user
        review_data['place'] = place
        review_data.pop('user_id', None)
        review_data.pop('place_id', None)

        try:
            review = Review(**review_data)

            place.add_review(review)
            
            self.review_repo.add(review)
            return review
        except (TypeError, ValueError) as e:
            raise ValueError(f"Review creation failed: {e}")

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(data)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)