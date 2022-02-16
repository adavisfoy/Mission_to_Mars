# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:35:28 2022

@author: Doanie
"""

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup as soup
"""import scraping"""

""" Set up Flask """
app = Flask(__name__)

"""Tell Python how to connect to Mongo using PyMongo"""
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

"""Set up Flask app routes: 1 - main HTML page, 2 - scrape new data"""
"""These routes can be embedded into our web app and accessed via links or buttons."""

"""HTML page route"""
"""This function links our web app to the code that powers it"""
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

"""Web Scraping route"""
"""Will be tied to a button that will run the code when clicked"""
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

"""Tell Flask to run"""
if __name__ == "__main__":
   app.run()