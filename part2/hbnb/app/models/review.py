#!/usr/bin/python3
"""
Review - HBnB review model
Respects UML encapsulation (- for private, + for public)
"""
from .basemodel import BaseModel
from .user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user, **kwargs):
        super().__init__(**kwargs)

        self._text = None
        self._rating = None
        self._place = None
        self._user = None

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        if hasattr(place, 'add_review'):
            place.add_review(self)


    @property
    def text(self): return self._text

    @property
    def rating(self): return self._rating

    @property
    def place(self): return self._place

    @property
    def user(self): return self._user


    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("Review text is required.")
        self._text = value

    @rating.setter
    def rating(self, value):
        if not isinstance(value, (int, float)) or not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        self._rating = int(value)

    @place.setter
    def place(self, value):

        if value is None:
            raise ValueError("Review must be linked to a Place.")
        self._place = value

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise ValueError("Review author must be a User instance.")
        self._user = value


    def update_rating(self, new_rating):
        """Mise à jour via le setter pour garantir la validation"""
        self.rating = new_rating
        self.save()