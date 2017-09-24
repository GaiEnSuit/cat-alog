#!/usr/bin/python3

import os
import sys

# SQLalchemy Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Instantiate declarative base
Base = declarative_base()

# table for users
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

# table for cats
class Cat(Base):
    __tablename__ = 'cat'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    category = Column(String(250), nullable=False)
    user = relationship(User)

# create databse
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

# bind engine to database
Base.metadata.bind = engine

# session for initial data
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add new user to database
theCreator = User(name='The Creator',
                  email='OmnipotentOne@gmail.com')

session.add(theCreator)

# Add new cat to databse
round = Cat(name='Round',
            image='https://sociorocketnewsen.files.wordpress.com/2013/10/maru-top.jpg',
            description='He likes boxes',
            category='Fat Cat',
            user=theCreator)

session.add(round)

# Add second cat to databse
wigglesborth = Cat(name='WigglesBorth',
                   image='http://www.cinemacats.com/wp-content/uploads/movies/austinpowersint05.jpg',
                   description='Cat of Dr No So Evil',
                   category='Hairless Cat',
                   user=theCreator)

session.add(wigglesborth)

# commit changes to databse
session.commit()