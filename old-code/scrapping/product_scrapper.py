from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import traceback

import re
import os

import urllib.request

from pymongo import MongoClient

from string import Template


driver = webdriver.Firefox(executable_path='./geckodriver') # initialize driver

client = MongoClient('localhost', 27017)
db = client['amazon_products']
products_collection = db['products']


#model
class Product():

	def __init__(self):
		self.product_name = ''
		self.attributes = {}		
		self.tags = list()

	def print_product(self):
		print('Product name: ', self.product_name)
		print('Product attributes: \n', self.attributes)
		print('Product tags: \n', self.tags)


#Issues to consider:
#1. The concept hierarchy provided by the website is not detailed enough
	# Scrap product description => Extract keywords => Build detailed hierarchy 
	# But how do we order the keywords?
#2. There should be a mechanism to prevent duplicate records from entering the database
	# One strategy could be digest the product name, and use that as id
#3. Despite of thorough checks, sometimes the image fails to be scrapped. Need a fallback option for this

#class which scraps products from database and adds record to mongo
	
class ProductScrapper():

	def __init__(self, input_file):
		self.input_file = input_file
		self.links = []
		self.attribute_pattern = re.compile("<\s*li[^>]*>(.*?)<\s*/\s*li>")
		self.scrapped_products = []
		self.possible_title_ids = ['productTitle', 'ebooksProductTitle']
		self.possible_image_ids = ['landingImage', 'imgBlkFront', 'ebooksImgBlkFront']

	def preprocess(self,val):
		val = val.replace("\"","")
		val = val.replace(".", "_")
		val = val.replace("/", "|")
		
		return val

	def scrape_product(self, link):
		p = Product()
		driver.get(link)

		#scrape product title
		found = False
		for title_id in self.possible_title_ids:
			try:
				title_element = driver.find_element_by_id(title_id)
				found = True
			except:
				continue
			if found:
				break
		if found == False:
			writer = open('error-log.txt', 'a')
			writer.write('ProductNameNotFoundError: '+ link + '\n')
			return
		p.product_name = self.preprocess(title_element.text)
		
		#scrap properties
		properties_element = driver.find_element_by_class_name('content')
		inner_html = properties_element.get_attribute('innerHTML')

		p.attributes = self.parse_properties(inner_html)
		tag_ref = driver.find_element_by_id('wayfinding-breadcrumbs_feature_div')
		tag_content = tag_ref.get_attribute('innerHTML')

		p.tags = self.parse_tags(tag_content)
		p.print_product()

		#scrap product image
		found = False
		for image_id in self.possible_image_ids:
			print('trying id : ', image_id)
			try:
				self.image_retriever_utility(image_id,p.product_name)
				found = True
			except:
				traceback.print_exc()
				continue
			if found:
				print(image_id, ' is valid')
				break
		if found == False:
			writer = open('error-log.txt', 'a')
			writer.write('ImageNotFoundError: '+ link + '\n')
			#terminate or go on?

		self.scrapped_products.append(p)
		#os.system("mv *.jpg ./images")	#move all images
		
	def image_retriever_utility(self, image_id,product_name):
		

		search_stub = Template("//img[@id='$img_id']")
		query = search_stub.substitute(img_id=image_id)
		print("Query = " , query)
		image_tag = driver.find_element_by_xpath(query)
		src = image_tag.get_attribute('src')
		product_image = product_name + '.jpg'
		urllib.request.urlretrieve(src, product_image)
		
		#os.system("mv " + "\"" + product_image + "\"" + ' ./images/')
	

	def parse_properties(self,inner_html):
		list_pattern = '</ul>'
		
		table_pattern = '</table>'

		response = {}
		if inner_html.find(list_pattern) != -1:
			print('Detected list structure')
			filtered_content = inner_html.split('<ul>')[1].split('</ul>')[0]
			#print(filtered_content)
			entries = self.attribute_pattern.findall(filtered_content)
		
					
			for entry in entries:
				key = entry.split('<b>')[1].split('</b>')[0]
				key = key.replace('\n', '')
				key = key.replace('.', '_')
				key = key.replace(':', '')
				value = entry.split('</b>')[1]
				value = value.replace('\n', '')
				value = value.replace('.', '')
				response[key] = value

		elif inner_html.find(table_pattern) != -1:
			print('Detected table structure')
			filtered_content = inner_html.split('<table')[1].split('</table>')[0]
			
			entries = filtered_content.split('</tr>')
			for entry in entries:
				entry = entry.strip()
				#<tr><td class="label"> OS </td><td class="value">Android</td></tr>

				print('Current entry: ', entry)
				try:
					t_list = entry.split('</td>')
					#print('t_list: ', t_list)
					key,value = self.parse_t_list(t_list)
					
					response[key] = value
				except:
					#print('Error while parsing row: ', entry)
					#traceback.print_exc()
					continue
		try:
			del response['&nbsp;']
			del response['']
		except KeyError:
			print('Filtered')
								
		return response

	def parse_t_list(self,t_list):
		#utility function for parsing the rows of table type product descriptions
		key = ''
		value = ''
		state = 0
		for val in t_list:
			if val.find('<td') == -1:
				continue
			else:
				try:
					if state == 0:
						key = val.split('>')[-1]
						state = 1
					else:
						value = val.split('>')[-1]
						break
				except:
					traceback.print_exc()
		key = key.replace('.', '_')
		value = value.replace('.', '_')
		return key,value

	def parse_tags(self,tag_content):
		parse_list = tag_content.split('</a>')
		tags = []
		for item in parse_list:
			try:
				value = item.split('<a')[1].split('>')[1].split('</a>')[0]
				value = value.replace('\n', '')
				value = value.replace(' ', '')	#Replace more than one whitespaces by one whitespace
				value = value.replace('&amp;', ' and ')
				tags.append(value)
			except:
				#print('Error while parsing ', item)
				#traceback.print_exc()
				continue
		return tags		

	def run(self):
		reader = open(self.input_file)
		for line in reader:
			line = line.strip()
			driver.get(line)
			self.scrape_product(line)


	def get_products(self):
		return self.scrapped_products


class MapToMongo():

	def __init__(self):
		self.status = 0

	def add_records(self,products):
		for product in products:
			product_dict = self.dict_utility(product)
			products_collection.insert_one(product_dict)	
			
	def dict_utility(self, product):
		doc = dict()
		doc['product_name'] = product.product_name
		doc['attributes'] = product.attributes
		doc['tags'] = product.tags

		return doc
		

if __name__ == '__main__':
	p = ProductScrapper('links.txt')
	p.run()
	products = p.get_products()
	
	m = MapToMongo()
	m.add_records(products)
