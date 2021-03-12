# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
# Import pandas for reading table from html
import pandas as pd
import datetime as dt
#to add wait time in panda read html
import time
#traceback
import traceback

#Main function 
# Initialize the browser.
#Create a data dictionary.
#End the WebDriver and return the scraped data.

def scrape_all():
   # Initiate headless driver for deployment
   #browser = Browser("chrome", executable_path="chromedriver", headless=True)
    # Windows users use the path to chrome drive
    executable_path = {
            'executable_path': 'c:/Users/covid19/Downloads/chromedriver_win32/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Get the latest news articlet title and summary
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()
        }

    # Stop webdriver and return data
    browser.quit()
    return data

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
    try:
        # We'll  assign the title and summary text to variables we'll reference later.
        slide_elem = new_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first <a> tag and use content tyile and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_title

        #Use the parent element to fnd the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        news_p
    except AttributeError:
        
        return None, None
    return news_title, news_p



# Featured Image funtion
# ### JPL Space Images Featured Images
def featured_image(browser):
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

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    except AttributeError:
        return None
    # add the base URL to the image URL from HTML to make an absolute URL
    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

#Code for the facts table will be updated in a similar manner to the other two. 
# # This time, though, we'll be adding BaseException to our except block for error handling.
def mars_facts():
    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
        time.sleep(1)
    except BaseException:
        traceback.print_exc() ## added to troubleshoot
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()



if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




