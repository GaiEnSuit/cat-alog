#!/usr/bin/python3

# Flask setup
from flask import Flask, render_template, redirect, url_for, request, jsonify, session as login_session, make_response
app = Flask(__name__)

# SQLalchemy Import
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, User, Cat

# Python Libraries
import json, httplib2

# Authorization Imports
from google.oauth2 import id_token
from google.auth.transport import requests

# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Home Route
@app.route('/')
def home():
    categories = session.query(Cat.category).distinct()
    cats = session.query(Cat).all()
    return render_template('/index.html', cats=cats, categories=categories)


# Sorted Home Route
@app.route('/<chosenCategory>/')
def sorted(chosenCategory):
    categories = session.query(Cat.category).distinct()
    cats = session.query(Cat).filter_by(category=chosenCategory).all()
    return render_template('/index.html',
                           cats=cats, categories=categories,
                           chosenCategory=chosenCategory)


# Route for new data
@app.route('/new/', methods=['GET', 'POST'])
def newCat():
    if request.method == 'POST':
        newCat = Cat(name=request.form['name'],
                     description=request.form['description'],
                     category=request.form['category'])
        session.add(newCat)
        session.commit()
        return redirect('/', code=302)
    else:
        return render_template('/new.html')


# Route for detailed item
@app.route('/<int:id>/detail/')
def detailCat(id):
    detailCat = session.query(Cat).filter_by(id=id).one()
    return render_template('/detail.html', i=detailCat)


# Route to edit item
@app.route("/<int:id>/edit/", methods=['GET', 'POST'])
def editCat(id):
    editedCat = session.query(Cat).filter_by(id=id).one()
    if request.method == 'POST':
        editedCat.name = request.form['name']
        editedCat.description = request.form['description']
        editedCat.category = request.form['category']
        session.add(editedCat)
        session.commit()
        return redirect('/', code=302)
    else:
        return render_template('/edit.html', i=editedCat)


# Route to delete item
@app.route('/<int:id>/delete/')
def deleteCat(id):
    deletedCat = session.query(Cat).filter_by(id=id).one()
    session.delete(deletedCat)
    session.commit()
    return redirect('/')


# Login In Route
@app.route('/login', methods=['POST'])
def logIn():
    # Client ID
    CLIENT_ID = "453291100677-8rb7dji1pcvpvu2hqpp5idr6n4e3o22d.apps.googleusercontent.com"
    # Receive HTTPS data
    token = request.args.get("id_token")
    # Validate ID Token
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    # Validate Issuer
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')
    # ID token is valid. Get the user's Google Account ID from the decoded token.
    login_session['sub'] = idinfo['sub']
    login_session['name'] = idinfo['name']
    login_session['email'] = idinfo['email']
    return "success"


# Create new user
def createUser(userID, userName, userEmail):
    newUser = User(name=userName, id=userID, email=userEmail)
    session.add(newUser)
    session.commit()
    return

# JSON API
@app.route('/JSON/')
def allCatJson():
    queriedCats = session.query(Cat).all()
    return jsonify(cats=[i.serialize for i in queriedCats])


@app.route('/<int:id>/JSON/')
def oneCatJSON(id):
    cat = session.query(Cat).filter_by(id=id).one()
    return jsonify(cat.serialize)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
