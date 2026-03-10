#!/usr/bin/python3
"""
Place - HBnB place model mapped to the database
"""
from app import db
from .basemodel import BaseModel

class Place(BaseModel):
    """
    Represents a place in the HBnB system, stored in the database.
    """
    __tablename__ = 'places'

    _title = db.Column('title', db.String(100), nullable=False)
    _description = db.Column('description', db.String(255))
    _price = db.Column('price', db.Float, nullable=False)
    _latitude = db.Column('latitude', db.Float, nullable=False)
    _longitude = db.Column('longitude', db.Float, nullable=False)
    _owner_id = db.Column('owner_id', db.String(36), nullable=False)

    def __init__(self, title, price, longitude, latitude, owner_id, description="", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.price = price
        self.longitude = longitude
        self.latitude = latitude
        self.owner_id = owner_id # On passe l'ID ici
        self.description = description

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title required (maximum 100 characters).")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("Price must be an integer or of a float.")
        if value <= 0:
            raise ValueError("Price must be positive.")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("Latitude must be an integer or a float.")
        if not -90 <= value <= 90:
            raise ValueError("latitude -90 to 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("Longitude must be an integer or a float.")
        if not -180 <= value <= 180:
            raise ValueError("longitude -180 to 180")
        self._longitude = float(value)

    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not isinstance(value, str):
            raise ValueError("owner_id must be a string (UUID).")
        self._owner_id = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
