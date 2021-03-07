#improt python dependancies
from flask import Flask, render_template
from flask_pymongo import PyMongo 
#import package form current application
import scraping

#initial app
app = Flask(__name__)

#use pymonog to setup mongo connection
# add mongo URI uniform resource identifier in the app config.
app.config["MONGI_URI"] = "mongodb://localbost:27017/mars_app"
mongo = PyMongo(app)

## Setup the Route for the web page. 
# One one for the main HTML page everyone will view when visiting the web app, 
# #and one to actually scrape new data using the code we've written.

#first route for main page 
@app.route("/")
def index():
    #main page shows the results from the latest mongo db results
    mars = mongo.db.mars.find_one()
    # render the index html page with data populated from mongo db
    return render_tempalte("index.html", mars = mars)

# 2nd route is when the scrape code run to scrape latest info and refresh the index
@app.route("/scrape")
def scrape():
   #setup variable to point to mongo db collection 
   mars = mongo.db.mars
   #run the scraping and retur the data to variable mars_data
   mars_data = scraping.scrape_all()
   #update mongodb with new data
   mars.update({}, mars_data, upsert=True)
   #go back to main page to show the latest info
   return redirect('/', code=302)

#The final bit of code we need for Flask is to tell it to run
if __name__ == "__main__":
   app.run(debug = True) #use debug true for debugging and running in dev 
