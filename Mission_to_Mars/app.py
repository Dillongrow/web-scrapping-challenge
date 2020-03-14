from flask import Flask, render_template, redirect 
import pymongo
import scrape_mars
import os

app = Flask(__name__)
#mongo = PyMongo(app, uri= "mongodb://localhost:27017/mars_app")

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_info


@app.route("/scrape")
def scrape(): 

    mars = scrape_mars.scrape()
    db.mars_info.insert_one(mars)

    return redirect("/", code=302)


@app.route("/")
def home(): 

    mars = list(db.mars_info.find())
    return render_template("index.html", mars_info=mars)

if __name__ == "__main__": 
    app.run(debug= True)