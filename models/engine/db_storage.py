#!/usr/bin/python3
'''Create a new storage method'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.state import State


class DBStorage:
    '''Stores all the data in mysql database'''

    __engine = None
    __session = None

    def __init__(self) -> None:
        usr, passwd = getenv('HBNB_MYSQL_USER'), getenv('HBNB_MYSQL_PWD')
        host, db = getenv('HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB')
        connection = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            usr, passwd, host, db)
        self.__engine = create_engine(connection,
                                      pool_pre_ping=True)
        if (getenv('HBNB_ENV') == 'test'):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        dict = {}
        if cls is not None:
            print('----------------')
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(cls.__class__.__name__, cls.id)
                dict[key] = obj
                print('key:',key)
        else:
            classes = [City, State]
            for cls in classes:
                query = self.__session.query(cls).all()
                for obj in query:
                    key = "{}.{}".format(
                        cls.__class__.__name__, cls.id
                    )
                    dict[key] = obj
                    print('key:',key)

        print('here is dict:',dict)
        return dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current database session obj if not None'''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''reloads the database'''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()
