from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_all():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = news(browser)
    mars_data ={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":image(browser),
        "mars_weather":weather(browser),
        "mars_facts":mars_facts(),
        "hemisphere_image_urls":hemisphere_image(browser)
    }
    browser.quit()
    return(mars_data)

def news(browser):
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_li = soup.find("li", class_="slide")
    news_title = news_li.find("div", class_="content_title")
    news_title = news_title.find("a").text
   
    news_paragraph = news_li.find("div", class_ ="article_teaser_body").text
    return(news_title,news_paragraph)

   

def image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    full_imagebtn = browser.find_by_id("full_image")
    full_imagebtn.click()
    time.sleep(2)
    full_infobtn = browser.find_link_by_partial_text("more info")
    full_infobtn.click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    base_url= "https://www.jpl.nasa.gov"
    featured_image_url = soup.find("article")
    featured_image_url = featured_image_url.find("img").get("src")
    featured_image_url = base_url + featured_image_url
    return(featured_image_url)

def weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
  
    tweets = soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    
    return(mars_weather)


def mars_facts():
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_df = pd.read_html(mars_facts_url)[1]
    mars_facts_df.columns = ["description","value"]
    mars_facts_df = mars_facts_df.to_html(classes = "table table-striped")

    return(mars_facts_df)

def hemisphere_image(browser):
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
        
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
        
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        hemi_dict['title'] = hemi_name.strip()
        
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)

    return(hemi_dicts)