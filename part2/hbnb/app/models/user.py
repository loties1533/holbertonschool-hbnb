#!/usr/bin/python3
"""
User - HBnB user model
Fields: first_name(max 50), last_name(max 50), email, is_admin(bool)
Relationships: owner of Places (1:N)
"""
from .basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, **kwargs):
        super().__init__(**kwargs)
        if not first_name or len(first_name) > 50:
            raise ValueError("First name required.")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name required.")
        if not email or '@' not in email:
            raise ValueError("Valid email required.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = kwargs.get('is_admin', False)
