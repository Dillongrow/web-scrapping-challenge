from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 
import pymongo

def init_browser():
    exec_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', headless=False, **exec_path)

def scrape():
        browser = init_browser()
        mars_info = {}
        
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        html = browser.html
        news_soup = BeautifulSoup(html, 'html.parser')
        news_title = news_soup.find_all('div', class_='content_title')[0].text
        news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

        main_url = 'https://www.jpl.nasa.gov'
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)
        html_image = browser.html
        image_soup = BeautifulSoup(html_image, 'html.parser')
        featured_image_path  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        featured_image_url = main_url + featured_image_path

        facts_url = 'http://space-facts.com/mars/'
        mars_facts = pd.read_html(facts_url)
        mars_df = mars_facts[2]
        mars_df.columns = ['Description','Value']
        mars_df.set_index('Description', inplace=True)
        data = mars_df.to_html()
        data.replace('\n', '')

        hemispheres_main_url = 'https://astrogeology.usgs.gov' 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        html_hemispheres = browser.html
        hemi_soup = BeautifulSoup(html_hemispheres, 'html.parser')
        items = hemi_soup.find_all('div', class_='item')
        hiu = []

        for i in items: 
            title = i.find('h3').text
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + partial_img_url)
            partial_img_html = browser.html
            hemi_image_soup = BeautifulSoup( partial_img_html, 'html.parser')
            img_url = hemispheres_main_url + hemi_image_soup.find('img', class_='wide-image')['src']
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "facts": str(data),
            "hemisphere_images": hiu
        }

        return mars_info