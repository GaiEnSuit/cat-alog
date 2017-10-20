#!/usr/bin/python3

# Flask setup
from flask import Flask, render_template, redirect, url_for, request, jsonify, session as login_session, make_response
app = Flask(__name__)

# SQLalchemy Import
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, User, Cat

# Python Libraries
import json
import httplib2
import requests

# Authorization Imports
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Set Secret Key
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


# Home Route
@app.route('/')
def home():
    categories = session.query(Cat.category).distinct()
    cats = session.query(Cat).all()
    if 'sub' not in login_session:
        return render_template('/index.html', cats=cats, categories=categories)
    else:
        return render_template('/index.html',
                               cats=cats,
                               categories=categories,
                               id=login_session['sub'])


# Sorted Home Route
@app.route('/<chosenCategory>/')
def sorted(chosenCategory):
    categories = session.query(Cat.category).distinct()
    cats = session.query(Cat).filter_by(category=chosenCategory).all()
    if 'sub' not in login_session:
        return render_template('/index.html',
                               cats=cats, categories=categories,
                               chosenCategory=chosenCategory)
    else:
        return render_template('/index.html',
                               cats=cats,
                               categories=categories,
                               id=login_session['sub'])


# Route for new data
@app.route('/new/', methods=['GET', 'POST'])
def newCat():
    if request.method == 'POST' and 'sub' in login_session:
        newCat = Cat(name=request.form['name'],
                     description=request.form['description'],
                     category=request.form['category'],
                     user_id=login_session['sub'])
        session.add(newCat)
        session.commit()
        return redirect('/', code=302)
    else:
        if 'sub' not in login_session:
            return redirect('/', code=302)
        else:
            return render_template('/new.html')


# Route for detailed item
@app.route('/<int:id>/detail/')
def detailCat(id):
    detailCat = session.query(Cat).filter_by(id=id).one()
    if 'sub' not in login_session:
        return render_template('/detail.html', i=detailCat)
    else:
        return render_template('/detail.html',
                               i=detailCat,
                               id=login_session['sub'])


# Route to edit item
@app.route("/<int:id>/edit/", methods=['GET', 'POST'])
def editCat(id):
    if request.method == 'POST' and 'sub' in login_session:
        editedCat = session.query(Cat).filter_by(id=id).one()
        if editedCat.user_id == login_session['sub']:
            editedCat.name = request.form['name']
            editedCat.description = request.form['description']
            editedCat.category = request.form['category']
            session.add(editedCat)
            session.commit()
            return redirect('/', code=302)
        else:
            return redirect('/', code=302)
    else:
        if "sub" not in login_session:
            return redirect('/', code=302)
        else:
            editedCat = session.query(Cat).filter_by(id=id).one()
            return render_template('/edit.html', i=editedCat)


# Route to delete item
@app.route('/<int:id>/delete/', methods=['GET', 'POST'])
def deleteCat(id):
    if request.method == 'POST' and 'sub' in login_session:
        deletedCat = session.query(Cat).filter_by(id=id).one()
        if login_session['sub'] == deletedCat.user_id:
            session.delete(deletedCat)
            session.commit()
            return redirect('/', code=302)
        else:
            return redirect('/', code=302)
    else:
        return redirect('/', code=302)


# Login In Route
@app.route('/login', methods=['POST'])
def logIn():
    if request.method == 'POST':
        # Please Set Your Client ID here
        CLIENT_ID = "453291100677-8rb7dji1pcvpvu2hqpp5idr6n4e3o22d.apps.googleusercontent.com"
        # Receive HTTPS data
        data = request.get_json()
        token = data['idtoken']
        try:
            # Validate ID Token
            idinfo = id_token.verify_oauth2_token(token, grequests.Request(), CLIENT_ID)
            # Validate Issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            # ID token is valid. Get the user's profile info from the decoded token.
            else:
                login_session['sub'] = idinfo['sub']
                login_session['name'] = idinfo['name']
                login_session['email'] = idinfo['email']
                if session.query(User).filter_by(id = idinfo['sub']).first() == None:
                    newUser = User(id=idinfo['sub'], name=idinfo['name'], email=idinfo['email'])
                    session.add(newUser)
                    session.commit()
                    return redirect("/", code=302)
                else:
                    return redirect("/", code=302)
        except ValueError:
            pass
        return redirect("/", code=302)
    else:
        return redirect("/", code=302)


# Logout In Route
@app.route('/logout')
def logOut():
    del login_session['sub']
    del login_session['name']
    del login_session['email']
    return redirect("/", code=302)


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
    app.run(host='0.0.0.0', port=80)
