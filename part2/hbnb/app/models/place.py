#!/usr/bin/python3
from .basemodel import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title=None, description=None, price=None, latitude=None, longitude=None, owner=None, **kwargs):
        super().__init__(**kwargs)
        self._amenities = []
        self._reviews = []


        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str) or len(value) > 100:
            raise ValueError("Title required (max 100 chars).")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):

        self._description = value if value is not None else ""

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is None:
            raise ValueError("Price is required.")
        if not isinstance(value, (float, int)) or value < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if value is None:
            raise ValueError("Latitude is required.")
        try:
            val = float(value)
            if not (-90.0 <= val <= 90.0):
                raise ValueError()
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a number between -90 and 90.")
        self._latitude = val

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if value is None:
            raise ValueError("Longitude is required.")
        try:
            val = float(value)
            if not (-180.0 <= val <= 180.0):
                raise ValueError()
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a number between -180 and 180.")
        self._longitude = val

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):

        if value is not None and not isinstance(value, User):
             raise ValueError("Owner must be a User instance.")
        self._owner = value

    @property
    def amenities(self):
        return self._amenities

    @property
    def reviews(self):
        return self._reviews

    def add_amenity(self, amenity):
        if amenity not in self._amenities:
            self._amenities.append(amenity)

    def add_review(self, review):
        if review not in self._reviews:
            self._reviews.append(review)