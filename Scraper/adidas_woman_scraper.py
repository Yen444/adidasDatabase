
from os import link
from turtle import clear
from bs4 import BeautifulSoup
  
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import urllib
import os
import re
import json
from check_robots_adidas import checkUrl
import copy

driver = webdriver.Chrome()

def getPageInformation(url): 
   """
   scrape info of each product
   """
   driver.get(url) 
   html = driver.page_source
   # this renders the JS code and stores all of the information in static HTML code.
   soup = BeautifulSoup(html, "xml")
   # or use xpath to find other single elements
   # num_reviews
   try:
      num_reviews = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div[2]/div[2]/div[1]/div[1]/button').text 
   except NoSuchElementException:
      pass
      num_reviews = 0
   # num_stars
   try:
      num_stars = driver.find_element(by=By.XPATH, value='//*[@id="navigation-target-reviews"]/div/button/div[1]/div/div/span').text
   except NoSuchElementException:
      pass
      num_stars = 0

   # price 
   try:
      price = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div')
      price = price.text
      price = float(price.replace('€', '').replace(',', '.').strip())      
   except NoSuchElementException:
      pass
      price = 0
   except ValueError:
      pass
      price = 5555

   # original price
   try: 
      price_old = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[1]')
      price_old = price_old.text 
      price_old = float(price_old.replace('€', '').replace(',', '.').strip())
   except NoSuchElementException:
      pass
      price_old = 0
   except ValueError:
      pass
      price_old = 5555

   # sale price
   try:
      price_sale = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[2]')
      price_sale = price_sale.text 
      price_sale = float(price_sale.replace('€', '').replace(',', '.').strip())
   except NoSuchElementException:
      pass
      price_sale = 0 
   except ValueError:
      pass
      price_sale = 5555
   # use html to look for colors
   if soup.find('div', class_="color-label___2hXaD"):
      color = soup.find('div', class_="color-label___2hXaD").text
   elif soup.find('div', class_="single-color-label___29kFh"):
      color = soup.find('div', class_="single-color-label___29kFh").text
   else:
      color = ''

   # use html to look for name
   if soup.find('h1', class_= 'name___120FN'):
      name = soup.find('h1', class_= 'name___120FN').text
   elif soup.find('h1', {"data-auto-id":"product-title"}):
      name = soup.find('h1', {"data-auto-id":"product-title"}).text
   else:
      name = ''
   # write everything to info dict
   info = {
      'name':name,
      'price':price,
      'price_old': price_old,
      'price_sale': price_sale,
      'color': color,
      'num_rev': num_reviews,
      'num_star': num_stars,
      'url': url,
      'brand': 'adidas',
      'for_gender': 1

   }
   return info

def extractUrls(url):
   """
   This function takes a base url (men/woman shoes) and returns a list of urls for products
   """
   list_links = []
   driver.get(url) 
   # scrolling down to extract all urls
   max_height = driver.execute_script("return document.body.scrollHeight")
   while driver.execute_script('return window.pageYOffset;') < max_height:
      driver.execute_script('window.scrollTo(0, window.pageYOffset + document.body.scrollHeight/5);')
      if driver.execute_script('return window.pageYOffset;') + driver.execute_script("return document.body.scrollHeight")/5 > max_height:
         break
   # this renders the JS code and stores all of the information in static HTML code.
   html = driver.page_source
   # Now, we could simply apply bs4 to html variable
   soup = BeautifulSoup(html, "xml")
   # and search
   links = soup.find_all('a', class_="product-card-content-badges-wrapper___2RWqS")
   for link in links:
      link = urllib.parse.urljoin(url, link.get('href'))
      list_links.append(link)
   return list_links

def extractNextPage(url):
   """
   Take url and return last page information(if this is last page) and link to next page
   """
   driver.get(url) 
   # this renders the JS code and stores all of the information in static HTML code.
   html = driver.page_source
   # Now, we could simply apply bs4 to html variable
   soup = BeautifulSoup(html, "xml")
   # and search
   l = soup.find('a', {"data-auto-id":"plp-pagination-next"})
   if l is None:
      next_page = None
   else:
      next_page = urllib.parse.urljoin(url, soup.find('a', {"data-auto-id":"plp-pagination-next"}).get('href'))
   return next_page

def main():
   shoe_women_dict_without_review = []
   base_url = 'https://www.adidas.de/frauen-schuhe'
   driver.get(base_url)

   # accept cookies for the very first time
   accept_button = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/button[1]/span')
   accept_button.click()
   time.sleep(0.5)

   page_count = 1
   shoe_count = 0
   while True:
      # extract next page
      next_page = extractNextPage(base_url)
      if next_page is None:
         print('This is the last page')
         break
      links = extractUrls(base_url)
      for link in links:
         print(link)
         # check if it is allowed to scrape the url or not
         allow = checkUrl(link)
         print(f'scraping allowed: {allow}')
         if allow == True:
            info = getPageInformation(link)
            shoe_women_dict_without_review.append(copy.deepcopy(info))
            shoe_count += 1
      print(f'Finishing page {page_count}')
      print(f'next page: {next_page}')
      base_url = next_page
      page_count += 1
      print(f'Successfully scraped {shoe_count} shoes')
   with open('/Users/yentran/sum2023/textTech/adidas_database/json_files/shoe_women_dict_adidas_without_review.json', 'w', encoding='utf-8') as file:
         json.dump(shoe_women_dict_without_review, file, indent=4) 
   driver.close()
if __name__ == "__main__":
    main()
