#!/usr/bin/python3
from .basemodel import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        super().__init__(**kwargs)
        self._amenities = []
        self._reviews = []
        
        # Initialisation via les setters pour profiter des validations
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    # --- TITLE ---
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title required (max 100 chars).")
        self._title = value

    # --- DESCRIPTION (La correction de ton bug) ---
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value if value else ""

    # --- PRICE ---
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (float, int)) or value <= 0:
            raise ValueError("Price must be a positive number.")
        self._price = float(value)

    # --- LATITUDE ---
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not (-90.0 <= float(value) <= 90.0):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = float(value)

    # --- LONGITUDE ---
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not (-180.0 <= float(value) <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = float(value)

    # --- OWNER ---
    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise ValueError("Owner must be a User instance.")
        self._owner = value

    # --- RELATIONS ---
    @property
    def amenities(self):
        return self._amenities

    @property
    def reviews(self):
        return self._reviews

    def add_amenity(self, amenity):
        if amenity not in self._amenities:
            self._amenities.append(amenity)
            self.save()

    def add_review(self, review):
        if review not in self._reviews:
            self._reviews.append(review)
            self.save()