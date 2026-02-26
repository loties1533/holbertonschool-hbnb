#!/usr/bin/python3
"""
BaseModel - HBnB base class for all models
Fields: id(UUID), created_at, updated_at
Methods: save/delete/get/get_all/update/to_dict (repo integration)
"""
import uuid
from datetime import datetime


class BaseModel:
    def __init__(self, **kwargs):

        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

        for key, value in kwargs.items():
            if key == "id":
                self._id = value
            elif key == "created_at":
                self._created_at = datetime.fromisoformat(value) if isinstance(value, str) else value
            elif key == "updated_at":
                self._updated_at = datetime.fromisoformat(value) if isinstance(value, str) else value

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    def save(self):
        """
        Met à jour le timestamp de modification
        """
        self._updated_at = datetime.now()

    def update(self, data):
        """
        Met à jour les attributs à partir d'un dictionnaire
        """
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:

                attr_name = f"_{key}" if hasattr(self, f"_{key}") else key
                setattr(self, attr_name, value)
        self.save()

    def to_dict(self):
        """
        Prépare les données pour JSON
        """
        result = {}
        for attr, value in self.__dict__.items():
            key = attr.lstrip('_') 
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result