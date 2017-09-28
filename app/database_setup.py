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
    description = Column(String(250), nullable=False)
    category = Column(String(250), nullable=False)
    user = relationship(User)

# create database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
