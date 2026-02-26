#!/usr/bin/python3
"""
Place - HBnB listing model
Fields: title, description, price, lat/lng, owner
Relationships: reviews(1:N), amenities(N:N)
"""
from .basemodel import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, description, price, longitude, latitude, owner, **kwargs):
        super().__init__(**kwargs)

        if not title or len(title) > 100:
            raise ValueError("Title required (max 100 chars).")
        if not isinstance(price, (float, int)) or price <= 0:
            raise ValueError("Price must be a positive number.")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance.")

        self._title = title
        self._description = description or ""
        self._price = float(price)
        self._longitude = float(longitude)
        self._latitude = float(latitude)
        self._owner = owner
        self._amenities = []
        self._reviews = []

    @property
    def title(self): return self._title
    
    @property
    def description(self): return self._description
    
    @property
    def price(self): return self._price
    
    @property
    def longitude(self): return self._longitude
    
    @property
    def latitude(self): return self._latitude
    
    @property
    def owner(self): return self._owner

    @property
    def amenities(self): return self._amenities

    @property
    def reviews(self): return self._reviews

    def add_amenity(self, amenity):
        if amenity not in self._amenities:
            self._amenities.append(amenity)
            self.save()

    def remove_amenity(self, amenity):
        if amenity in self._amenities:
            self._amenities.remove(amenity)
            self.save()

    def add_review(self, review):
        if review not in self._reviews:
            self._reviews.append(review)
            self.save()