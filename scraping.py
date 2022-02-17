# Import Splinter, Beautiful Soup, Chrome dev tools, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set executable path and browser / Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Article Scraping

# Assign URL and instruct browser to visit it
# Visit Mars new site
url = 'https://redplanetscience.com'
browser.visit(url)

# Search for elements with a specific combination of tag (div) and attribute (list_text). 
# As an example, ul.item_list would be found in HTML as <ul class="item_list">.
# Also telling our browser to wait one second before searching for components. 
# The optional delay is useful because sometimes dynamic pages take a little while to load, esp. if image heavy
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object / Set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# We'll want to assign the title and summary text to variables we'll reference later. 
# Let's begin our scraping. 
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the summary text - Tag div, class 'article_teaser_body'
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Featured Images

# Tag <img class="headerimage fade-in"
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

# Mars Facts

# Mars facts are in table format
# Use Pandas .read_html() function to scrape the entire table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Convert DataFrame back to html for web app
df.to_html()

# Shut down automated browser
browser.quit()