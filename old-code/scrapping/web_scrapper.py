from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import traceback
driver = webdriver.Firefox(executable_path='./geckodriver')
class WebScrapper():

	def __init__(self, input_file='amazon_links.txt', output_file='amazon_product_links.txt'):
		self.input_file = input_file
		self.output_file = output_file

	def scrape(self):

		reader = open(self.input_file)

		writer = open(self.output_file, 'a')
		for link in reader:
			try:
				link = link.strip()
				print('Trying: ', link)				
				driver.get(link)
				# a class=""
				for i in range(0,5):	#rep counts
					prod_links = driver.find_elements_by_xpath("//a[@href]")
					for prod_link in prod_links:
						link_val = prod_link.get_attribute('href')
						print(link_val)
						writer.write(link_val+'\n')
						#links.append(link_val)
			
					next_button = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
					next_button.click()
			except:
				#traceback.print_exc()
				continue
		
			

if __name__ == "__main__":
	ws = WebScrapper()
	ws.scrape()
