from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

def init_browser():

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    browser = init_browser()
    mars_dict = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    title = soup.find("div", class_="content_title").get_text()
    paragraph = soup.find("div", class_="article_teaser_body").get_text()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    images = soup.find('article', class_='carousel_item')['style']
    featured = images.split("'")
    featured_image = "https://www.jpl.nasa.gov" + featured[1]

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    df = pd.read_html("https://space-facts.com/mars/")
    mars_df = df[0]
    super_mars_df = mars_df.to_html(index=False, header=False)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    h3_ = []
    link = []
    images = []
    dicts = []
    
    results = soup.find_all('div', class_='item')

    for result in results:
        h3 = result.find('h3').text
        h3_.append(h3)
        
        href = result.find('a')['href']
        the_link = f'https://astrogeology.usgs.gov{href}'
        link.append(the_link)
    
        browser.visit(the_link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        result = soup.find('div', class_='downloads')
        image = result.find('a')['href']
        images.append(image)

        hem = {"h3": h3, "image": image}
        dicts.append(hem)
        
    mars_dict = {"title": title, "paragraph": paragraph, "featured_image": featured_image, "super_mars_df": super_mars_df, "dicts": dicts}
    
    return mars_dict


