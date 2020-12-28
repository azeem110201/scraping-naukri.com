from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import re

PATH = "C:\Program Files (x86)\chromedriver.exe"

search_1 = input("Enter the job name or company name:")
number_of_jobs = int(input("Enter the number of job opening:"))
query = input(
    "enter the location. press 'y' if any or 'n' if any location is okay:")
search_2 = list()
url = str()

if query == 'y':
	print("press 'none' if no more location to give")
	while "none" not in search_2:
		location = input("Enter location...")
		search_2.append(location)

	sub_string = str()

	for i in search_2:
		if i != "none":
			sub_string = sub_string + i + "-"

	url = "https://www.naukri.com/" + search_1 + "-jobs-in-" + sub_string
	print(url)
if	query == 'n':
	url = "https://www.naukri.com/" + search_1 + "-jobs-in-"
print(url)

driver = webdriver.Chrome(PATH)
driver.get(url)
driver.implicitly_wait(10)

results = pd.DataFrame()
results['title'] = np.nan
results['company'] = np.nan
results['years'] = np.nan
results['salary'] = np.nan
results['links'] = np.nan

a = 0
b = 0
c = 0
d = 0

number_of_jobs = number_of_jobs // 20

for i in range(1,number_of_jobs):
	for elem in driver.find_elements_by_xpath("//a[contains(@class, 'title fw500 ellipsis')]"):
		results.loc[a, 'links'] = elem.get_attribute('href')
		results.loc[a,'title'] = elem.text
		a += 1

	for elem in driver.find_elements_by_xpath("//a[contains(@class, 'subTitle ellipsis fleft')]"):
		results.loc[b,'company'] = elem.text
		b += 1

	some_list = list()
	main_list = list()

	for elem in driver.find_elements_by_xpath("//span[contains(@class, 'ellipsis fleft fs12 lh16')]"):
		some_list.append(elem.text)

	i = 0
	for elements in some_list:
		main_list.append(some_list[i:i+3])
		i += 3
    
	for z in range(len(main_list)):
		try:
			if re.search(r'Yrs\b', main_list[z][0]):
				results.loc[c,'years'] = main_list[z][0]
				c += 1
		except Exception as e:
			pass

	patterns = [r'.*\b(disclosed)$', r'.*\b(PA.)$']
	for z in range(len(main_list)):
		try:
			for pattern in patterns:
				pm = re.compile(pattern)
				has = pm.match(main_list[z][1])
				if has:
					results.loc[d,'salary'] = main_list[z][1]
					d += 1
		except Exception as e:
			pass				

	button = driver.find_element_by_id('root')
	button.click()
	driver.implicitly_wait(10)

results.to_csv("results.csv")
print("done")