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
#from webdriver_manager.chrome import ChromeDriverManager
import sys
import argparse
from selenium.webdriver.support.ui import Select

def parse_auto(Inputdictionary,bool_check):
	'''parser = argparse.ArgumentParser()
	parser.add_argument("--list", nargs="+", default=83843)
	args = parser.parse_args()
	print(args.list)'''

	chrome_options = Options()
	chrome_options.add_argument("--headless")
	#s=Service(ChromeDriverManager().install())
	#driver = webdriver.Chrome(service=s)
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
		NewDict['startYear1']= 1980
	elif 'searchRadius' not in NewDict or 'searchRadius1' not in NewDict:
		NewDict['searchRadius1'] = 100
	elif 'price' not in NewDict or 'price1' not in NewDict:
		NewDict['price1'] = 1000
	print(NewDict)


	if len(bool_check)==0:
		if 'searchRadius' not in NewDict and len(NewDict)<=3:
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars?zip={NewDict['zip']}&makeCodeList={NewDict['makeCodeList']}&modelCodeList={NewDict['modelCodeList']}")
		elif 'searchRadius' in NewDict and len(NewDict)==2:
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars/moscow-id-{NewDict['zip']}?dma=&searchRadius={NewDict['searchRadius1']}&isNewSearch=true&marketExtension=include&showAccelerateBanner=false&sortBy=relevance&numRecords=25")
		elif 'searchRadius' in NewDict and len(NewDict)>2:
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars/{NewDict['makeCodeList'].lower()}/{NewDict['modelCodeList'].lower()}/moscow-id-{NewDict['zip']}?dma=&searchRadius={NewDict['searchRadius']}&isNewSearch=true&marketExtension=include&showAccelerateBanner=false&sortBy=relevance&numRecords=25")
		else:
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars/cars-over-10000/moscow-id-{NewDict['zip']}?dma=&searchRadius=50&priceRange=&location=&startYear=2007&marketExtension=include&extColorsSimple=BLACK&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25")
	else:
		if ('year1>=' in bool_check or 'year1>' in bool_check) and len(bool_check)==1:
			print('11')
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars/{NewDict['makeCodeList'].lower()}/{NewDict['modelCodeList'].lower()}/moscow-id-{NewDict['zip']}?dma=&searchRadius={NewDict['searchRadius1']}&location=&startYear={NewDict['startYear1']}&marketExtension=include&endYear=2020&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25")
		elif ('price1>=' in bool_check or 'price1>' in bool_check) and 'searchRadius' in NewDict:
			print('22')
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars/cars-over-{NewDict['price1']}/moscow-id-{NewDict['zip']}?dma=&searchRadius={NewDict['searchRadius1']}&priceRange=&location=&startYear={NewDict['startYear1']}&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25")
		elif ('price2<=' in bool_check or 'price2<' in bool_check) and ('price1>=' in bool_check or 'price1>' in bool_check) and 'searchRadius' in NewDict:
			print('33')
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars/cars-between-{NewDict['price1']}-and-{NewDict['price2']}/moscow-id-{NewDict['zip']}?dma=&searchRadius={NewDict['searchRadius1']}&priceRange=&location=&startYear={NewDict['startYear1']}&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25")
		elif ('price2<=' in bool_check or 'price2<' in bool_check):
			print('44')
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars/cars-under-{NewDict['price2']}/moscow-id-{NewDict['zip']}?dma=&searchRadius=50&priceRange=&location=&startYear={NewDict['startYear1']}&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25")
		else:
			driver.get(f"https://www.autotrader.com/cars-for-sale/all-cars/cars-over-{NewDict['price1']}/moscow-id-{NewDict['zip']}?dma=&searchRadius=50&priceRange=&location=&startYear={NewDict['startYear1']}&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25")
	try:

		'''soup = BeautifulSoup(driver.page_source, "html.parser")
		driver.close()
		select_tag1 = soup.find("select", attrs={'id': '2230463214'})
		options1 = select_tag1.find_all("option")
		allcars = []
		for option in options1:
			if option.text != 'Any Make':
				allcars.append(option.text.upper())'''
		#print("Any Make", allcars)
		##zip code
		'''zip = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/form/div/div[3]/div/div/input')))
		zip.clear()
		zip.send_keys("83843")
		time.sleep(1)
	
		##carmake
		element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="2230463214"]')))
		element.click()
		option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='2230463214']/optgroup[1]/option[@value='HONDA']")))
		option.click()
		time.sleep(1)
	
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/form/div/div[4]/button'))).click()
		time.sleep(1)
		newWindow = driver.window_handles[0]
		driver.switch_to.window(newWindow)
		time.sleep(1)
		print(driver.current_url)
		#select = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div/form/div/div[1]/div/select"))))
		#select = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="2230463214"]'))))
		#print(select.select_by_value("HONDA"))
		#driver.find_element('//*[@id="mountNode"]/div[1]/div[2]/div/div/div/div[1]/div/form/div/div[1]/div').send_keys("HONDA")'''
		#while true:

		#element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mountNode"]/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[3]')))
		#final_element1 = driver.find_element_by_xpath('//*[@id="mountNode"]/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[3]').find_elements_by_xpath('.//*')
		final_element1 = driver.find_element_by_xpath('//*[@id="mountNode"]/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[3]')
		c = final_element1.find_elements_by_xpath("./child::*")

		if NewDict['makeCodeList'] == 'HONDA':
			final_data = []
			for g,h in enumerate(c):
				if c[g].text != '':
					data = c[g].text.split('Used')
			#data = c[1].text.split('Used') + c[4].text.split('Used')

			data = [ele for ele in data if ele.strip()]
			for i in data:
				final_dict = {"year": i.lstrip().split(' ')[0], "price": i.lstrip().split('\n')[1],"miles": i.lstrip().split('\n')[2]}
				final_data.append(final_dict)
		else:
			data_1 =[]
			data_2 = []
			final_data = []
			for i in range(len(c)):
				data_2= data_2 + c[i].text.split('Used')
				'''start = c[i].text.strip().find("Used") + len("Used")
				end = c[i].text.strip().find("Availability")
				data_1.append(c[i].text.strip()[start:end])'''
				s = c[i].text.strip().replace('\r\n','').replace('\n',' ')
				#print(c[i].text,"string is",s)
				m = re.match(r'Used(.*?)Availability', s)
				if m:
					data_1.append(m.group(0))
			data_1 = [ele for ele in data_1 if ele.strip()]

			for i in data_1:
				d = i.lstrip().split(' ')
				final_dict = {"year": d[1],"price":d[5],"miles":d[6]}
				final_data.append(final_dict)

		#print(final_data)

		return final_data
	except TimeoutException:
		print("TimeoutException: Element not found")

	driver.close()
	'''
	
	select_tag1 = soup.find("select",attrs={'id':'2230463214'})
	select_tag2 = soup.find("select",attrs={'id':'1617644117'})
	
	# find all option tag inside select tag
	
	options2 = select_tag2.find_all("option")
	
	# Iterate through all option tags and get inside text
	allcars=[]
	allmodels=[]
	
	# Step 2: Create a parse tree of page sources after searching
	soup = BeautifulSoup(driver.page_source, "lxml")
	
	
	
	for option in options2:
		#if option.text!='Any Model':
		allmodels.append(option.text)
'''

def main():
	InputDict = {'makeCodeList': 'FORD', 'modelCodeList': 'EDGE', 'zip': '83843'}

	parse_auto(InputDict,['year>=2020'])


if __name__ == "__main__":
    main()