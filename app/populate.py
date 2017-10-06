#!/usr/bin/python3

# Imports
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, User, Cat

# bind engine to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# session for initial data
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add new cat to databse
round = Cat(name='Round',
            description='He likes boxes',
            category='fat')

session.add(round)

# Add second cat to databse
wigglesborth = Cat(name='WigglesBorth',
                   description='Cat of Dr No So Evil',
                   category='hairless')

session.add(wigglesborth)

# commit changes to databse
session.commit()
