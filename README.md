# Mission To Mars - Latest News and Facts

## Project Overview:
The web page Mission to Mars scrapes latest news , pictures and facts about mars from different websites and present this information in a nice layout.

## Solution overview:

- Create python functions to Scrape data as follows:
    - Latest Mars news from https://mars.nasa.gov/news/
    - Latest Mars featured image from https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html
    - Mars Facts from http://space-facts.com/mars/
- Save the results in Mongo DB
- Create a web app using Flask with following features:
    - Rendered scraped data from Mongo DB on the root using Bootstrap for styling via a index.html
    - A button to "Scrape New Data" for user to scrapes latest information.

### Challenge:

- Scrape High-Resolution Mars Hemisphere Images and Titles
- Update the Web App with Mars Hemisphere Images and Titles
- Add Bootstrap 3 Components


## Resources
In addtion to abvove mentiond websites used for scraping data , following tools were used 
- Python: Anaconda Python 3.7 , panda , Splinter, Beautiful Soup , Flask, Web driver manager
- Web app : Using Flask framework , PyMongo
- Database : Monog Db
- Chromedriver 

## Code

- Final Scrape code: [Scrape Code](scraping.py)
- Final web app code: [Web app code](app.py)
- HTML for root: [Web app HTML](templates\index.html)

- For challenge first deliverabl where Mars hemispheres were published using full image the html code is saved in [Backup html code for full images](\templates\Full_Image_D2_index.html)


## Instruction to run the Code:

### Widnows:

1. Install Mongo Db using documenation https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
2. Install python liberaries in your python enviornment.
    - pip install splinter
    - pip install bs4 
    - pip install html5lib
    - pip install lxml
    - pip install webdriver_manager
    - pip install flask
3. Chromedriver from https://chromedriver.chromium.org/downloads Use the latest one based on your chrome version isntalled your machine. Also edit the location of Chrome driver file in the scrapping.py code.
4. Run the app from the anaconda enviornment using Falsk run <full path to app.py> or use set Flask app = app.py and run Flask run from the folder where the app.py is located
