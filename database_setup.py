#!/usr/bin/python3

# For environment variables
import sys

# SQLAlchemy Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('sqlite///catalog.db')
