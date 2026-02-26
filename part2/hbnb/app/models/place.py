#!/usr/bin/python3
from .basemodel import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, description, price, longitude, latitude, owner, **kwargs):
        super().__init__(**kwargs)
        self._amenities = []
        self._reviews = []
        self._description = description or ""
        
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title required (max 100 chars).")
        self._title = value

    @property
    def price(self): return self._price
    @price.setter
    def price(self, value):
        if not isinstance(value, (float, int)) or value <= 0:
            raise ValueError("Price must be a positive number.")
        self._price = float(value)

    @property
    def latitude(self): return self._latitude
    @latitude.setter
    def latitude(self, value):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude between -90 and 90.")
        self._latitude = float(value)

    # ... idem pour longitude et owner ...

    @property
    def amenities(self): return self._amenities

    def add_amenity(self, amenity):
        if amenity not in self._amenities:
            self._amenities.append(amenity)
            self.save()