#!/usr/bin/python3
"""
BaseModel - HBnB base class for all models
Fields: id(UUID), created_at, updated_at
Methods: save/delete/get/get_all/update/to_dict (repo integration)
"""
import uuid
from datetime import datetime
from app.persistence.repository import InMemoryRepository

_repository = InMemoryRepository()

class BaseModel:
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    
    def save(self):
        self.updated_at = datetime.now()

    def delete(self):
        _repository.delete(self.id)

    @classmethod
    def get(cls, obj_id):
        return _repository.get(obj_id)

    @classmethod
    def get_all(self):
        return _repository.get_all()

    @classmethod
    def get_by_attribute(cls, attr_name, attr_value):
        return _repository.get_by_attribute(attr_name, attr_value)

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        result = {}
        for attr in self.__dict__:
            value = getattr(self, attr)
            if isinstance(value, datetime):
                result[attr] = value.isoformat()
            else:
                result[attr] = value
        return result
