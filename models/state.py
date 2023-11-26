#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base, BaseModel
from os import getenv


class State(BaseModel, Base):
    """ State class """

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        from sqlalchemy import Column, String
        from sqlalchemy.orm import relationship

        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City',
                              cascade='all, delete',
                              backref='state')
    else:
        name = ''

        @property
        def cities(self):
            '''returns the list of City instances with state_id
                equals the current State.id
                FileStorage relationship between State and City
            '''
            from models import storage
            related_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)
            return related_cities
