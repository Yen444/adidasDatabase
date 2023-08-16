import json
import pprint

import lxml.etree as ET
import numpy as np

from mongoengine import connect
connect(db='shoeDataset', host='localhost', port = 27017)
from mongoengine import Document, ListField, StringField, URLField, FloatField, BooleanField
from pymongo import MongoClient
from typing import Tuple, List, Dict


def create_statistic(query_result) -> Tuple[Dict[str, float], Dict[str, float]]:
   """
   Create complete statistics for men and woman products
   """

   result_dict_men = {}
   result_dict_women = {}

   prices_man = []
   prices_woman = []

   number_reviews_man = []
   number_reviews_woman = []

   price_drop_man = []
   price_drop_woman = []

   number_stars_man = []
   number_stars_woman = []

   number_with_review_women = 0
   number_with_review_men = 0 

   for entry in query_result:

      if entry["for_gender"] == 0:
         prices_man.append(float(entry["price"]))

         number_reviews = float(entry["num_rev"])
         number_reviews_man.append(number_reviews)
         if number_reviews > 0:
            number_with_review_men += 1

         number_stars_man.append(float(entry["num_star"]))

         if float(entry["price_sale"]) > 0:
            price_drop = (float(entry["price_sale"]) - float(entry["price"])) / float(entry["price"]) * 100
            price_drop_man.append(price_drop)
      else:
         prices_woman.append(float(entry["price"]))

         number_reviews = float(entry["num_rev"])
         if number_reviews > 0:
            number_with_review_women += 1
         
         number_reviews_woman.append(number_reviews)
         number_stars_woman.append(float(entry["num_star"]))

         if float(entry["price_sale"]) > 0:
            price_drop = (float(entry["price_sale"]) - float(entry["price"])) / float(entry["price"]) * 100
            price_drop_woman.append(price_drop)

   result_dict_men["prices"] = np.array(prices_man)
   result_dict_men["min_price"] = np.min(result_dict_men["prices"])
   result_dict_men["max_price"] = np.max(result_dict_men["prices"])
   result_dict_men["price_drop"] = np.array(price_drop_man)
   result_dict_men["mean"] = np.mean(prices_man)
   result_dict_men["median"] = np.median(prices_man)
   result_dict_men["stdev"] = np.std(prices_man)
   result_dict_men["number_reviews"] = np.array(number_reviews_man)
   result_dict_men["number_stars"] = np.array(number_stars_man)
   result_dict_men["mean_stars"] = np.mean(result_dict_men["number_stars"])
   result_dict_men["std_stars"] = np.std(result_dict_men["number_stars"])
   result_dict_men["min_stars"] = np.min(result_dict_men["number_stars"])
   result_dict_men["max_stars"] = np.max(result_dict_men["number_stars"])
   result_dict_men["number_products_with_review"] = number_with_review_men

   result_dict_women["prices"] = np.array(prices_woman)
   result_dict_women["min_price"] = np.min(result_dict_women["prices"])
   result_dict_women["max_price"] = np.max(result_dict_women["prices"])
   result_dict_women["price_drop"] = np.array(price_drop_woman)
   result_dict_women["mean"] = np.mean(prices_woman)
   result_dict_women["median"] = np.median(prices_woman)
   result_dict_women["stdev"] = np.std(prices_woman)
   result_dict_women["number_reviews"] = np.array(number_reviews_woman)
   result_dict_women["number_stars"] = np.array(number_stars_woman)
   result_dict_women["mean_stars"] = np.mean(result_dict_women["number_stars"])
   result_dict_women["std_stars"] = np.std(result_dict_women["number_stars"])
   result_dict_women["min_stars"] = np.min(result_dict_women["number_stars"])
   result_dict_women["max_stars"] = np.max(result_dict_women["number_stars"])
   result_dict_women["number_products_with_review"] = number_with_review_women


   return result_dict_men, result_dict_women


def create_histogram_in_xml(hist_element, number_bins : int, input_data : np.ndarray):

   bins, edges = np.histogram(input_data, bins=number_bins)
   # ignore last edge -> close enough
   edges = edges[:-1]

   for i in range(number_bins):
      bin = bins[i]
      edge = edges[i]

      hist_entry_element = ET.SubElement(hist_element, "Entry")
      bin_element = ET.SubElement(hist_entry_element, "edge")
      bin_element.text = f"{edge}"
      bin_element = ET.SubElement(hist_entry_element, "bin")
      bin_element.text = f"{bin}"

def insert_list_in_xml(root_node, elements : List[Tuple[np.ndarray, str]]):
   """
   Insert a list (each element can consists of multiple entries
   All arrays should have the same size, otherwise the smallest size will be taken
   """

   min_size = min([element[0].shape[0] for element in elements])

   for idx in range(min_size):
      entry_element = ET.SubElement(root_node, "Entry")
      for element in elements:
         value_array = element[0]
         element_name = element[1]
         price_element = ET.SubElement(entry_element, element_name)
         price_element.text = f"{value_array[idx]:.2f}"

def insert_json_into_database():
   """
   Clear database and insert data in json file into the database
   """

   client = MongoClient('localhost', 27017)
   db = client['shoeDatabase']

   # create new one
   db.drop_collection('shoeCollection')
   collection = db['shoeCollection']
   # insert man products
   with open('json_files/shoe_men_dict_adidas_without_review.json', 'r') as f:
      shoe_dataset_men = json.load(f)
      collection.insert_many(shoe_dataset_men)
   # insert woman products
   with open('json_files/shoe_women_dict_adidas_without_review.json', 'r') as f:
      shoe_dataset_women = json.load(f)
      collection.insert_many(shoe_dataset_women)


def create_xml_file():
   """
   creat one xml file containing data for statistics, histogram and scatter plot
   """
   client = MongoClient('localhost', 27017)
   db = client['shoeDatabase']
   collection = db['shoeCollection']

   root = ET.Element("ShoeResults")

   # find everything
   result = collection.find({})
   # create statistics dict
   men_dict, woman_dict = create_statistic(result)
   # write statistics into xml file
   statistics_element_men = ET.SubElement(root, "StatisticsMan")
   median_element = ET.SubElement(statistics_element_men, "Median")
   median_element.text = f"{men_dict['median']:.2f}"
   mean_element = ET.SubElement(statistics_element_men, "Mean")
   mean_element.text = f"{men_dict['mean']:.2f}"
   stdev_element = ET.SubElement(statistics_element_men, "Stdev")
   stdev_element.text = f"{men_dict['stdev']:.2f}"
   number_products_element = ET.SubElement(statistics_element_men, "NumberProducts")
   number_products_element.text = f"{len(men_dict['prices'])}"
   number_sale_products_element = ET.SubElement(statistics_element_men, "NumberSaleProducts")
   number_sale_products_element.text = f"{len(men_dict['price_drop'])}"
   mean_stars_element = ET.SubElement(statistics_element_men, "MeanStars")
   mean_stars_element.text = f"{men_dict['mean_stars']:.2f}"
   stdev_stars_element = ET.SubElement(statistics_element_men, "StdevStars")
   stdev_stars_element.text = f"{men_dict['std_stars']:.2f}"
   min_stars_element = ET.SubElement(statistics_element_men, "MinStars")
   min_stars_element.text = f"{men_dict['min_stars']:.2f}"
   max_stars_element = ET.SubElement(statistics_element_men, "MaxStars")
   max_stars_element.text = f"{men_dict['max_stars']:.2f}"
   min_price_element = ET.SubElement(statistics_element_men, "MinPrice")
   min_price_element.text = f"{men_dict['min_price']:.2f}"
   max_price_element = ET.SubElement(statistics_element_men, "MaxPrice")
   max_price_element.text = f"{men_dict['max_price']:.2f}"
   number_with_review_element = ET.SubElement(statistics_element_men, "NumberProductsWithReview")
   number_with_review_element.text = f"{men_dict['number_products_with_review']}"

   statistics_element_woman = ET.SubElement(root, "StatisticsWomen")
   median_element = ET.SubElement(statistics_element_woman, "Median")
   median_element.text = f"{woman_dict['median']:.2f}"
   mean_element = ET.SubElement(statistics_element_woman, "Mean")
   mean_element.text = f"{woman_dict['mean']:.2f}"
   stdev_element = ET.SubElement(statistics_element_woman, "Stdev")
   stdev_element.text = f"{woman_dict['stdev']:.2f}"
   number_products_element = ET.SubElement(statistics_element_woman, "NumberProducts")
   number_products_element.text = f"{len(woman_dict['prices'])}"
   number_sale_products_element = ET.SubElement(statistics_element_woman, "NumberSaleProducts")
   number_sale_products_element.text = f"{len(woman_dict['price_drop'])}"
   mean_stars_element = ET.SubElement(statistics_element_woman, "MeanStars")
   mean_stars_element.text = f"{woman_dict['mean_stars']:.2f}"
   stdev_stars_element = ET.SubElement(statistics_element_woman, "StdevStars")
   stdev_stars_element.text = f"{woman_dict['std_stars']:.2f}"
   min_stars_element = ET.SubElement(statistics_element_woman, "MinStars")
   min_stars_element.text = f"{woman_dict['min_stars']:.2f}"
   max_stars_element = ET.SubElement(statistics_element_woman, "MaxStars")
   max_stars_element.text = f"{woman_dict['max_stars']:.2f}"
   min_price_element = ET.SubElement(statistics_element_woman, "MinPrice")
   min_price_element.text = f"{woman_dict['min_price']:.2f}"
   max_price_element = ET.SubElement(statistics_element_woman, "MaxPrice")
   max_price_element.text = f"{woman_dict['max_price']:.2f}"

   number_with_review_element = ET.SubElement(statistics_element_woman, "NumberProductsWithReview")
   number_with_review_element.text = f"{woman_dict['number_products_with_review']}"

   # write histogram values for man to xml
   prices_men = men_dict["prices"]
   hist_element_men = ET.SubElement(root, "HistogramMan")
   create_histogram_in_xml(hist_element_men, 20, prices_men)

   # write histogram values for women to xml
   prices_woman = woman_dict["prices"]
   hist_element_woman = ET.SubElement(root, "HistogramWomen")
   create_histogram_in_xml(hist_element_woman, 20, prices_woman)


   # write prices, number reviews, and number stars in xml file to create 
   # a scatter plot afterwards
   prices_element_men = ET.SubElement(root, "RawDataMan")
   input_elements = [(men_dict["prices"], "Price"), (men_dict["number_reviews"], "NumberReviews"), ( men_dict["number_stars"], "NumberStars")]
   insert_list_in_xml(prices_element_men, input_elements)

   prices_element_woman = ET.SubElement(root, "RawDataWomen")
   input_elements = [(woman_dict["prices"], "Price"), (woman_dict["number_reviews"], "NumberReviews"), ( woman_dict["number_stars"], "NumberStars")]
   insert_list_in_xml(prices_element_woman, input_elements)

   tree = ET.ElementTree(root)
   with open ("xml/out.xml", "wb") as xml_file:
         tree.write(xml_file, pretty_print=True)

def create_html_file(xslt_template_filename : str, html_filename : str):
   """
   use pre-defined xslt files to transform xml to html files
   """
   dom = ET.parse("xml/out.xml")
   xslt = ET.parse(xslt_template_filename)
   transform = ET.XSLT(xslt)
   newdom = transform(dom)
   with open(html_filename, "w") as html_file:
      html_file.write(ET.tostring(newdom, pretty_print=True, encoding="unicode", method="html"))

   print("finished creating html file")


if __name__ == "__main__": 

   insert_json_into_database()
   create_xml_file()
   create_html_file("xslt/xlst_template_statistics.xml", "html/statistics.html")
   create_html_file("xslt/xlst_template_hist.xml", "html/histogram.html")
   create_html_file("xslt/xlst_template_scatter.xml", "html/scatter.html")
   
    

