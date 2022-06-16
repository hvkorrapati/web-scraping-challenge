# Import Dependencies

import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Function 

def scrape(): 
# Setup splinter

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    # url

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # html and bs 
    browser.is_element_present_by_css('div.list_text', wait_time=5)

    html = browser.html
    soup = bs(html, 'html.parser')

    # NASA Mars News -- two variables

    news_title = soup.find('div', class_ = 'content_title').text.strip()
    news_p = soup.find('div', class_ = 'article_teaser_body').text.strip()

    # JPL Mars Space Images—Featured Image

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('img', class_ = "headerimage fade-in")['src']

    featured_image_url = f"https://spaceimages-mars.com/{image}"

    # Mars Facts
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    tables = pd.read_html('https://galaxyfacts-mars.com')
    df = tables[1]
    table = df.to_html()
    table = table.replace('\n', '')

    # Mars Hemispheres

    img_url = ''
    title = ''

    hemi_list = ['cerberus',
                'valles',
                'schiaparelli',
                'syrtis']

    hemisphere_image_urls = []

    for x in range (0,4):
        url = f'https://marshemispheres.com/{hemi_list[x]}.html'
        browser.visit(url)

        html = browser.html
        soup = bs(html, 'html.parser')

        title = hemi_list[x]
        img_url = soup.find_all('li')[0].a['href']

        hemisphere_image_urls.append({"title": title, "img_url": f'https://marshemispheres.com/{img_url}'})

        img_url = ''
        title = ''

    # Quit Browser

    browser.quit()

    # Master Dictionary of all scraped data

    master_dict = {}
    master_dict['news_title'] = news_title
    master_dict['news_description'] = news_p
    master_dict['featured_image_url'] = featured_image_url
    master_dict['mars_facts'] = table
    master_dict['hemisphere_image_urls'] = hemisphere_image_urls


    return master_dict