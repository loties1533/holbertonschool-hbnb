#!/usr/bin/python3
"""
Place - HBnB listing model (Airbnb-style)
Fields: title(max 100), description, price, lat/lng, owner(User)
Relationships: reviews(1:N), amenities(N:N)
Methods: add/remove amenity/review
"""
from .basemodel import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, description, price, longitude, latitude, owner, **kwargs):
        super().__init__(**kwargs)

        if not title or len(title) > 100:
            raise ValueError("Title required.")

        if not isinstance(price, (float, int)):
            raise ValueError("Price must be an integer or of a float.")

        if price <= 0:
            raise ValueError("Price must be positive.")

        if not isinstance(latitude, (float, int)):
            raise ValueError("Latitude must be an integer or a float.")

        if not -90 <= latitude <= 90:
            raise ValueError("latitude -90 to 90")

        if not isinstance(longitude, (float, int)):
            raise ValueError("Longitude must be an integer or a float.")

        if not -180 <= longitude <= 180:
            raise ValueError("longitude -180 to 180")
            
        if not isinstance(owner, User):
            raise ValueError("owner must be User instance")

        self.title = title
        self.description = description or ""
        self.price = float(price)
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.owner = owner
        self.amenities = []
        self.reviews = []

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def remove_amenity(self, amenity):
        if amenity in self.amenities:
            self.amenities.remove(amenity)
            self.save()

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)
            self.save()
