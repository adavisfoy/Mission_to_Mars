# Import Splinter, Beautiful Soup, Chrome dev tools, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set executable path and browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Article Pieces

# Use original code within a function

def mars_news(browser):

    # Assign URL and instruct browser to visit it
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Search for elements with a specific combination of tag (div) and attribute (list_text). 
    # As an example, ul.item_list would be found in HTML as <ul class="item_list">.
    # Also telling our browser to wait one second before searching for components. 
    # The optional delay is useful because sometimes dynamic pages take a little while to load, esp. if image heavy

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try-except for error handling
    try: 
        # Let's begin our scraping.
        slide_elem = news_soup.select_one('div.list_text')
    
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the summary text - Tag div, class 'article_teaser_body'
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p
    
# ### Featured Images

# Refactor original code into function

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
    
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'   

    return img_url

# ### Mars Facts

def mars_facts():
    try:
        # Use Pandas .read_html() function to scrape the entire table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# Shut down automated browser
browser.quit()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# Set executable path and browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere
urls_titles = browser.find_by_css('a.product-item img')

for i in range(len(urls_titles)):
    
    hemisphere={}
    
    # Click on each hemisphere link to get to the full image
    browser.find_by_css('a.product-item img')[i].click()
    
    # Find 'Sample'/full-size image link - link contains the full-sized image
    # Don't need to click again - can get all the info from here
    sample_link = browser.links.find_by_text('Sample').first
    
    # Get hemisphere image link
    hemisphere['img_url'] = sample_link['href']
    
    # Get hemisphere Title 
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    # Add data from hemisphere dictionary to hemisphere_image_urls list
    # Output a list of dictionaries
    hemisphere_image_urls.append(hemisphere)
    
    # Go back in browser to get url and title for next image
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# Close down browser
browser.quit()


