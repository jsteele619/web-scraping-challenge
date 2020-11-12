from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
#db.collection

@app.route("/")
def index():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    list = scrape_mars.scrape()
    mars_dict.update({}, list, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


