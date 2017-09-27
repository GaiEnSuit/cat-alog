#!/usr/bin/python3

# Flask setup
from flask import Flask
from flask import render_template
app = Flask(__name__)

# SQlalchemy setup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, User, Cat

# Connect to databse
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    categories = session.query(Cat.category).distinct()
    cats = session.query(Cat).all()
    return render_template('/index.html', cats=cats, categories=categories)

@app.route('/<chosenCategory>/')
def sorted(chosenCategory):
    categories = session.query(Cat.category).distinct()
    cats = session.query(Cat).filter_by(category=chosenCategory).all()
    return render_template('/index.html', cats=cats, categories=categories, chosenCategory=chosenCategory)


@app.route('/new/')
def newCat():
    return render_template('/new.html')


@app.route('/<int:id>/detail/')
def detailCat(id):
    return render_template('/detail.html')


@app.route("/<int:id>/edit/")
def editCat(id):
    return render_template('/edit.html', id=id)


@app.route('/<int:id>/delete/')
def deleteCat(id):
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
