#!/usr/bin/python3

# Flask setup
from flask import Flask
app = Flask(__name__)

# SQlalchemy setup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, User, Cat

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def HelloWorld():
    return 'Hello World'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
