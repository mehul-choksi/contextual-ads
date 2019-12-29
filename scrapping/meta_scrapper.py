from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
driver = webdriver.Firefox(executable_path='./geckodriver')

class MetaScrapper():

	def __init__(self, url='http://www.amazon.in'):

		self.url = url
		self.links = list()
	def scrape(self):
		driver.get(self.url)
		# aria-label="Open Menu"
		button = driver.find_element_by_xpath("//a[@aria-label='Open Menu']")
		#button.click()

		#main_div = driver.find_element_by_xpath("//div[id='hmenu-content']")

		delay = 10 # seconds
		main_div = None
		try:
		    main_div = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'hmenu-content')))

		except TimeoutException:
		    print("Loading took too much time!")		
		inner_html = main_div.get_attribute('innerHTML')

		possible_links = inner_html.split("href=\"")

		for link in possible_links:
			link = link.split("\"")[0]
			self.links.append(link)
		writer = open('amazon_links.txt', 'w')
		for link in self.links:
			if link == '' or link == '/':
				continue
			elif link.startswith('/'):
				writer.write('http://www.amazon.in/' + link + '\n')
			else:
				writer.write(link + '\n')
if __name__ == '__main__':
	ms = MetaScrapper()
	ms.scrape()

