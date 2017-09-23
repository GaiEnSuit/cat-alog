#!/usr/bin/python3

import os
import sys

# SQLalchemy Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Instantiate declarative base
Base =  declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    

class Cat(Base):
    __tablename__ = 'cat'
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(250))
    image = Column (String(250))
    description = Column(String(250))

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)