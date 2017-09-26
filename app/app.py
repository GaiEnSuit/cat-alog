#!/usr/bin/python3

# Flask setup
from flask import Flask
from flask import render_template
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
@app.route('/<string:category>/')
def HelloWorld():
    cats = session.query(Cat).all()
    return render_template("/index.html", cats=cats)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
