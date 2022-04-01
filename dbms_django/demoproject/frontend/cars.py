# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 2021

@author: RashmiShrivastava

"""

from bs4 import BeautifulSoup
import time
import re
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import sys
import argparse
from selenium.webdriver.support.ui import Select


def parse_cars(Inputdictionary,bool_check):
    '''parser = argparse.ArgumentParser()
    parser.add_argument("--list", nargs="+", default=83843)
    args = parser.parse_args()
    print(args.list)'''

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(r'C:\chromedriver.exe')

    logging.basicConfig(filename='test_scrape.log', level=logging.INFO)

    ''' Parsing dictionary to create URL
    '''
    NewDict = {}
    for x in Inputdictionary:
        if 'zip' in x:
            NewDict['zip'] = Inputdictionary[x]
        elif 'make' in x:
            NewDict['makeCodeList'] = Inputdictionary[x]
        elif 'model' in x:
            NewDict['modelCodeList'] = Inputdictionary[x]
        elif 'mile' in x:
            NewDict['searchRadius1'] = Inputdictionary[x]
        elif 'mile1' in x:
            NewDict['searchRadius1'] = Inputdictionary[x]
        elif 'mile2' in x:
            NewDict['searchRadius2'] = Inputdictionary[x]
        elif 'year' in x:
            NewDict['startYear1'] = Inputdictionary[x]
        elif 'year1' in x:
            NewDict['startYear1'] = Inputdictionary[x]
        elif 'year2' in x:
            NewDict['startYear2'] = Inputdictionary[x]
        elif 'price' in x:
            NewDict['price1'] = Inputdictionary[x]
        elif 'price1' in x:
            NewDict['price1'] = Inputdictionary[x]
        elif 'price2' in x:
            NewDict['price2'] = Inputdictionary[x]
    if 'year' not in NewDict or 'year1' not in NewDict:
        NewDict['startYear1'] = 1980
    elif 'searchRadius' not in NewDict or 'searchRadius1' not in NewDict:
        NewDict['searchRadius1'] = 100
    elif 'price' not in NewDict or 'price1' not in NewDict:
        NewDict['price1'] = ''
    print(NewDict)

    #driver.get(f"https://www.cars.com/shopping/results/?stock_type=used&makes%5B%5D={search_keyword1.lower()}&models%5B%5D={search_keyword1.lower()}-{search_keyword2.lower()}&list_price_max=&maximum_distance=20&zip={search_keyword3}")
    #driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars?zip={search_keyword3}&makeCodeList={search_keyword1}&modelCodeList={search_keyword2}")
    # driver.get(f'https://www.autotrader.com/cars-for-sale/all-cars?zip=83843&makeCodeList=HONDA&modelCodeList=CIVIC')
    driver.get(f"https://www.cars.com/shopping/results/?stock_type=used&makes%5B%5D=honda&models%5B%5D={NewDict['makeCodeList'].lower()}-{NewDict['modelCodeList'].lower()}&list_price_max=&maximum_distance=50&zip={NewDict['zip']}")

    try:
        final_element1 = driver.find_elements_by_class_name('vehicle-details')
        #c = final_element1.find_elements_by_xpath("./child::*")
        final_data = []
        for j,i in enumerate(final_element1):
            if j>=1:
                miles = i.find_element_by_class_name('mileage').text
                price = i.find_element_by_class_name('primary-price').text
                year = i.text.split('Used')[1].replace('\n','').split(' ')[0]
                final_dict = {'miles':miles,'price':price,'year':year}
                final_data.append(final_dict)
            else:
                continue
        print(final_data)
        return final_data
    except TimeoutException:
        print("TimeoutException: Element not found")

    driver.close()

def main():
    parse_cars("FORD", "EDGE", search_keyword3=83843)


# parse_auto("HONDA", "CIVIC", search_keyword3=83843)


if __name__ == "__main__":
    main()