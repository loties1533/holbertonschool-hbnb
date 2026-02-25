#!/usr/bin/python3
"""
Amenity - HBnB amenity model
Fields: name (max 50 chars)
"""
from .basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Amenity name required, max 50 chars")
        self._name = value