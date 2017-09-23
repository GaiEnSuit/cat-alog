#!/usr/bin/python3

# Imports for sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import sessionmaker

# Import classes from database_setup
from database_setup import Base, User, Cat

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

theCreator = User(name='The Creator',
                  email='OmnipotentOne@gmail.com')

round = Cat(name='Round',
            image='https://sociorocketnewsen.files.wordpress.com/2013/10/maru-top.jpg',
            description='He likes boxes',
            category='Fat Cat',
            user=theCreator)

wigglesborth = Cat(name='WigglesBorth',
                   image='http://www.cinemacats.com/wp-content/uploads/movies/austinpowersint05.jpg',
                   description='Cat of Dr No So Evil',
                   category='Hairless Cat',
                   user=theCreator)

session.add_all(round, wigglesborth)
session.commit()
