#!/usr/bin/env python3
""" DataBase engine """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, NoResultFound
# from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import Base
from user import User


class DB():
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str):
        """ add new user to the DataBase """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """ Find User """
        if not kwargs:
            raise InvalidRequestError

        valid_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_columns:
                raise InvalidRequestError

        found_user = self._session.query(User).filter_by(**kwargs).first()
        if not found_user:
            raise NoResultFound

        return found_user
