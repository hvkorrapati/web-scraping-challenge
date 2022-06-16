import pymongo
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from scrape_mars import scrape
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)
mars_info = mongo.db.mars_data

@app.route("/")
def welcome():
    holding = mars_info.find_one()
    return render_template("index.html", stuff = holding)

@app.route("/scrape")
def scraping():
    results = scrape()

    mars_info.update_one({}, {"$set": results}, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)

