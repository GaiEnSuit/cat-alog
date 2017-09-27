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

# Add new user to database
theCreator = User(name='The Creator',
                  email='OmnipotentOne@gmail.com')

session.add(theCreator)

# Add new cat to databse
round = Cat(name='Round',
            image='https://sociorocketnewsen.files.wordpress.com/2013/10/maru-top.jpg',
            description='He likes boxes',
            category='Fat',
            user=theCreator)

session.add(round)

# Add second cat to databse
wigglesborth = Cat(name='WigglesBorth',
                   image='http://www.cinemacats.com/wp-content/uploads/movies/austinpowersint05.jpg',
                   description='Cat of Dr No So Evil',
                   category='Hairless',
                   user=theCreator)

session.add(wigglesborth)

# commit changes to databse
session.commit()
