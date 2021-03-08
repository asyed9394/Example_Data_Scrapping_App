# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
# Import pandas for reading table from html
import pandas as pd

# Windows users
# update the path to chrome drive
executable_path = {
    'executable_path': 'c:/Users/covid19/Downloads/chromedriver_win32/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# With the following line, browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1),
# we are accomplishing two things.

# One is that we're searching for elements with a specific combination of tag (ul and li)
# and attribute (item_list and slide, respectively). For example, ul.item_list would be found in HTML as <ul class=”item_list”>.

# Secondly, we're also telling our browser to wait one second before searching for components.
# The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# setup the html parse
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

# We'll  assign the title and summary text to variables we'll reference later.
slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ### JPL Space Images Featured Images

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Next, we want to click the "Full Image" button. This button will direct our browser to an image slideshow. Let's take a look at the button's HTML tags and attributes with the DevTools.
# 2nd button is the full image butting based on the search in the html code
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup from the above cell run
html = browser.html
img_soup = soup(html, 'html.parser')

# It's important to note that the value of the src will be different every time the page is updated,
# so we can't simply record the current value—we would only pull that image each time the code is executed,
# instead of the most recent one.
# We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# add the base URL to the image URL from HTML to make an absolute URL
# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

# ## Mars Facts

# Tables in HTML are basically made up of many smaller containers. The main container is the <table /> tag.
# Inside the table is <tbody />, which is the body of the table—the headers, columns, and rows.
# <tr /> is the tag for each table row. Within that tag, the table data is
# stored in <td /> tags. This is where the columns are established.
# Instead of scraping each row, or the data in each <td />,
# we're going to scrape the entire table with Pandas' .read_html() function.

# read table from html
# df = pd.read_html('http://space-facts.com/mars/')[0] With this line,
# we're creating a new DataFrame from the HTML table.
# The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML.
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
# read_html read tables from html
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns = ['description', 'value']
df.set_index('description', inplace=True)
df

# Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function.

df.to_html()

browser.quit()


# Scrape news from nasa mars news website
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #Convert the browser html to a soup object  
 
    html = browser.html
    new_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try
        # We'll  assign the title and summary text to variables we'll reference later.
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first <a> tag and use content tyile and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_title

        #Use the parent element to fnd the paragraph text
        news_p = slike_elem.find('div', class_="article_teaser_body").get_text()
        news_p
    except AttributeError:
        return None, None
    return news_title, news_p

