#!/usr/bin/python3
from .basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, **kwargs):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Name required.")
        self.name = name
