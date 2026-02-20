#!/usr/bin/python3
"""
Review - HBnB review model
Fields: text, rating(1-5), place(Place), user(User)
Relationships: belongs_to Place+User (auto-add via place.add_review)
Methods: update_rating
"""
from .basemodel import BaseModel
from .place import Place
from .user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user, **kwargs):
        super().__init__()

        if not text:
            raise ValueError("Text required.")
        if not 1 <= rating <= 5:
            raise ValueError("Rating from 1 to 5 required.")
        if not isinstance(place, Place):
            raise ValueError("place must be Place instance.")
        if not isinstance(user, User):
            raise ValueError("user must be User instance.")

        self.text = text
        self.rating = int(rating)
        self.place = place
        self.user = user

        place.add_review(self)

    def update_rating(self, new_rating):
        if 1 <= new_rating <= 5:
            self.rating = new_rating
            self.save()
