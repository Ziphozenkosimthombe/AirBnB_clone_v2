#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'updated_at':
                        self.updated_at = (datetime.strptime(
                            kwargs['updated_at'], "%Y-%m-%dT%H:%M:%S.%f"))
                    elif key == 'created_at':
                        self.created_at = (datetime.strptime(
                            kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        """Sets the named attribute on the given object
                        to the specified value.
                        """
                        setattr(self, key, value)

    def __str__(self):
        """returns a string
        Return:
            returns a string of class name, id, and dictionary
        """
        dic = self.to_dict()
        # del dic['__class__']
        # dic['created_at'] = datetime.strptime(dic['created_at'],
        #                                       "%Y-%m-%dT%H:%M:%S")
        # dic['updated_at'] = datetime.strptime(dic['updated_at'],
        #                                       "%Y-%m-%dT%H:%M:%S")
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, dic)

    def __repr__(self):
        """return a string representaion
        """
        return self.__str__()

    def save(self):
        """updates the public instance attribute updated_at to current
        """
        from models.__init__ import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        '''delete the current instance from the storage'''
        from models import storage
        storage.delete(self)
