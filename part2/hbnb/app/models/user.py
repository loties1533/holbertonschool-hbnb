#!/usr/bin/python3
import re
from .basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False, **kwargs):
        # Initialisation des attributs privés
        self._first_name = None
        self._last_name = None
        self._email = None
        self._is_admin = False

        super().__init__(**kwargs)

        # Utilisation des setters pour la validation immédiate
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        # On vérifie que ce n'est pas vide et que ça ne dépasse pas 50
        if not value or not isinstance(value, str) or len(value.strip()) == 0 or len(value) > 50:
            raise ValueError("First name required (maximum 50 characters).")
        self._first_name = value.strip()

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str) or len(value.strip()) == 0 or len(value) > 50:
            raise ValueError("Last name required (maximum 50 characters).")
        self._last_name = value.strip()
        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        # Regex améliorée : utilisateur@domaine.extension
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not value or not re.match(email_regex, value):
            raise ValueError("Invalid email format.")
        self._email = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean.")
        self._is_admin = value