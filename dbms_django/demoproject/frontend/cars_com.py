# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
url = 'https://www.cars.com/research/honda-civic-2020/'

response=requests.get(url,headers=headers)


soup=BeautifulSoup(response.content,'lxml')



car_title=soup.select('.sds-page-section__title')[0].get_text().strip()
print("Car name: " ,car_title)
print("Price: " ,soup.select('.sds-heading--4')[0].get_text().strip())
print("Rating: " ,soup.select('.rating__count')[0].get_text().strip())
print("Reviews: " ,soup.select('.rating__link')[0].get_text().strip())


print("")
print ('Badges for the ' ,car_title)
for badge in soup.select('.mmy-header__popular'):
	print(badge.get_text().strip())

print("")
print ('Features of the ' ,car_title)

for feature in soup.select('.list-features li'):
	print(feature.get_text().strip())

print("")
print ('What to know about ' ,car_title)

for whattoknow in soup.select('.list-checklist-label'):
	print(whattoknow.get_text().strip())

print("")
print ('News about ' ,car_title)

for news in soup.select('.list-article__item'):
	print(news.select('.list-article__title')[0].get_text().strip())
	print(news.select('.list-article__content')[0].get_text().strip())
	print(news.select('a')[0]['href'])