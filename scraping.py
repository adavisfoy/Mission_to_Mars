# Import Splinter, Beautiful Soup, Chrome dev tools, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # initiate headless driver for deployment
    # Set executable path and browser / Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


def hemispheres(browser):
    
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere
    # urls_titles = browser.find_by_css('a.product-item img')

    for i in range(4):
    
        hemispheres={}
    
        # Click on each hemisphere link to get to the full image
        browser.find_by_css('a.product-item img')[i].click()
    
        # Find 'Sample'/full-size image link - link contains the full-sized image
        # Don't need to click again - can get all the info from here
        sample_link = browser.links.find_by_text('Sample').first

        # Parse the resulting html with soup
        html = browser.html
        browser.links_soup = soup(html, 'html.parser')
        
        try: 
            # Get hemisphere image link
            hemispheres['img_url'] = sample_link['href']
    
            # Get hemisphere Title 
            hemispheres['title'] = browser.find_by_css('h2.title').text
        
        except AttributeError: 
            hemispheres['img_url'] = None
            hemispheres['title'] = None
    
        # Add data from hemisphere dictionary to hemisphere_image_urls list
        # Output a list of dictionaries
        hemisphere_image_urls.append(hemispheres)
        
        # Go back in browser to get url and title for next image
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

# Close down browser
# browser.quit()


# Article Scraping

# Assign URL and instruct browser to visit it
# Visit Mars new site
# url = 'https://redplanetscience.com'
# browser.visit(url)

# Search for elements with a specific combination of tag (div) and attribute (list_text). 
# As an example, ul.item_list would be found in HTML as <ul class="item_list">.
# Also telling our browser to wait one second before searching for components. 
# The optional delay is useful because sometimes dynamic pages take a little while to load, esp. if image heavy
# browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object / Set up html parser
# html = browser.html
# news_soup = soup(html, 'html.parser')
# slide_elem = news_soup.select_one('div.list_text')

# We'll want to assign the title and summary text to variables we'll reference later. 
# Let's begin our scraping. 
# slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
# news_title = slide_elem.find('div', class_='content_title').get_text()
# news_title

# Use the parent element to find the summary text - Tag div, class 'article_teaser_body'
# news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
# news_p

# Featured Images

# Tag <img class="headerimage fade-in"
# Visit URL
# url = 'https://spaceimages-mars.com'
# browser.visit(url)

# Find and click the full image button
# full_image_elem = browser.find_by_tag('button')[1]
# full_image_elem.click()

# Parse the resulting html with soup
# html = browser.html
# img_soup = soup(html, 'html.parser')

# Find the relative image url
# img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# img_url_rel

# Use the base URL to create an absolute URL
# img_url = f'https://spaceimages-mars.com/{img_url_rel}'

# Mars Facts

# Mars facts are in table format
# Use Pandas .read_html() function to scrape the entire table
# df = pd.read_html('https://galaxyfacts-mars.com')[0]
# df.columns=['description', 'Mars', 'Earth']
# df.set_index('description', inplace=True)
# df

# Convert DataFrame back to html for web app
# df.to_html()

# Shut down automated browser
# browser.quit()