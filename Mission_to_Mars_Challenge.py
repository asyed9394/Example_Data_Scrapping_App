#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#Import pandas for reading table from html
import pandas as pd
import time # to add sleep


# In[2]:


# Windows users
#update the path to chrome drive
executable_path = {'executable_path': 'c:/Users/covid19/Downloads/chromedriver_win32/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


#With the following line, browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1), 
#we are accomplishing two things.

#One is that we're searching for elements with a specific combination of tag (ul and li) 
#and attribute (item_list and slide, respectively). For example, ul.item_list would be found in HTML as <ul class=”item_list”>.

#Secondly, we're also telling our browser to wait one second before searching for components.
#The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.


# In[5]:


#setup the html parse
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


#We'll  assign the title and summary text to variables we'll reference later. 
slide_elem.find("div", class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Images

# In[44]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[10]:


#Next, we want to click the "Full Image" button. This button will direct our browser to an image slideshow. Let's take a look at the button's HTML tags and attributes with the DevTools.
# 2nd button is the full image butting based on the search in the html code
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1] 
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup from the above cell run
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[12]:


#It's important to note that the value of the src will be different every time the page is updated, 
#so we can't simply record the current value—we would only pull that image each time the code is executed, 
#instead of the most recent one.
#We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image. 
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


#add the base URL to the image URL from HTML to make an absolute URL
# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


#Tables in HTML are basically made up of many smaller containers. The main container is the <table /> tag.
#Inside the table is <tbody />, which is the body of the table—the headers, columns, and rows.
#<tr /> is the tag for each table row. Within that tag, the table data is
#stored in <td /> tags. This is where the columns are established.
#Instead of scraping each row, or the data in each <td />, 
#we're going to scrape the entire table with Pandas' .read_html() function.


# In[36]:


#read table from html
#df = pd.read_html('http://space-facts.com/mars/')[0] With this line,
#we're creating a new DataFrame from the HTML table. 
#The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML.
#By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
df = pd.read_html('http://space-facts.com/mars/')[0] #read_html read tables from html
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[16]:


# Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function. 

df.to_html()


# ### D1: Scrape High Resolution Mars' Hemisphere Images and Titles

# In[3]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[5]:


######################################## TESTING CODE FOR RETRIEVING TITELS ###################################################
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.
#setup the html parse
html = browser.html
news_soup = soup(html, 'html.parser')

titles_list =[]
h3_data = news_soup.find_all('h3')
for h3 in h3_data:
    title =  h3.text 
    title
    titles_list.append(title)
titles_list


# In[12]:


#############################TESTING CODE For retreiving image ################################################################
##based on html inspection, we can see that full image file is not found on the first page. The first image is a thumb nail png
# the full pciture full.jpg is found after clicking on the link for each thumnail 
# step a is to find  href releated to the tiltes found in the title tags and
# step b then click on the link using browser obejct link.find_by_href.click()
#note that browser.links.find_by_href return a list, so alwasy ensure to use first or index to choose where to click
# Step c from the 2nd page get the image file name from tag li and use href from tag 1save it to a list
# step d go back to main page and then repeat step a and step c for all 4 occurances of tag a  (title)

image_list= []
div_data = news_soup.find_all('div', class_='item')
for x in range( len(titles_list)):

    link = div_data[x].find('a')['href']
    browser.links.find_by_href(link).last.click()
    time.sleep(5) # add delay as browser could take time to load full html
    #full_url_for_next_page = 'https://astrogeology.usgs.gov'+ div_data[x].find('a')['href']
    
    #image_list.append(link)
    #print(browser.click_link_by_partial_href(link))
    #browser.links.find_by_partial_href(link).click() #error ElementNotInteractableException
    #browser.links.find_by_partial_text(link).click() #error ElementDoesNotExist: no elements could be found with link by partial text "/search/map/Mars/Viking/cerberus_enhanced"
    #browser.links.find_by_text(link).click() #error ElementDoesNotExist: no elements could be found with link by text "/search/map/Mars/Viking/cerberus_enhanced"
    #browser.links.find_by_href(link).click() #error ElementNotInteractableException: Message: element not interactable: element has zero size
    #driver.wait()
    
    html=browser.html
    image_soup = soup(html, 'html.parser')
    div = image_soup.find('div', class_='downloads')
    image = div.find('a')['href']
    image_list.append(image)
    browser.back()
image_list


# In[16]:


#####################CODE FOR THE DELIVERABLE 1 the above 2 cells are for testing purposes######################################
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
#setup the html parse
html = browser.html
news_soup = soup(html, 'html.parser')

#Extract title based on the html inspection, title is saved in the h3 tag . there are only four h3 tag so we can use that to 
#get the titels . in addition for image URL we need to click
div_data = news_soup.find_all('div', class_='item')
for div in div_data:
    title = div.find('h3').text
    link = div.find('a')['href']
    browser.links.find_by_href(link).last.click()
    time.sleep(5) # add delay as browser could take time to load full html
    html=browser.html
    image_soup = soup(html, 'html.parser')
    image_div = image_soup.find('div', class_='downloads')
    image = image_div.find('a')['href']
    hemisphere_image_urls.append({
        'image_url' : image,
        'title' : title        
        })
    browser.back()
hemisphere_image_urls


# In[17]:


browser.quit()


# In[ ]:




