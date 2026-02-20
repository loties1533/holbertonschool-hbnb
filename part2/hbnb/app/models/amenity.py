#!/usr/bin/python3
"""
Amenity - HBnB amenity model (Wi-Fi, Parking, etc.)
Fields: name(max 50)
Relationships: many-to-many with Place (Place.add_amenity)
"""
from .basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, **kwargs):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Name required.")
        self.name = name
