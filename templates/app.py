from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Mission_to_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mission_to_Mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info = mars_info)


@app.route("/scrape")
def scraped():
    mars_info = mongo.db.mars_info
    mars_data = Mission_to_mars.scrape()
    mars_info.insert_many(mars_data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
