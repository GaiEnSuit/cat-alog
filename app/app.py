#!/usr/bin/python3

# Flask setup
from flask import Flask, render_template, redirect, url_for, request
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


@app.route('/new/', methods=['GET', 'POST'])
def newCat():
    if request.method == 'POST':
        newCat = Cat(name=request.form['name'], description=request.form['description'], category=request.form['category'])
        session.add(newCat)
        session.commit()
        return redirect('/', code=302)
    else:
        return render_template('/new.html')


@app.route('/<int:id>/detail/')
def detailCat(id):
    return render_template('/detail.html')


@app.route("/<int:id>/edit/", methods=['GET', 'POST'])
def editCat(id):
    editedCat = session.query(Cat).filter_by(id=id).one()
    if request.method == 'POST':
        editedCat.name=request.form['name']
        editedCat.description=request.form['description']
        editedCat.category=request.form['category']
        session.add(editedCat)
        session.commit()
        return redirect('/', code=302)
    else:
        return render_template('/edit.html', i = editedCat)


@app.route('/<int:id>/delete/')
def deleteCat(id):
    deletedCat = session.query(Cat).filter_by(id=id).one()
    session.delete(deletedCat)
    session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
