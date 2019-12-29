from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import traceback
driver = webdriver.Firefox(executable_path='./geckodriver')

class RawFilesMaker():
	def __init__(self, input_file):
		self.input_file = input_file

	#mechanism to deal with broken links
	def save_htmls(self):
		reader = open(self.input_file)
		i = 3175
		count = 0
		for line in reader:
			if count < i:
				count += 1
				continue
			line = line.strip()
			driver.get(line)
			i += 1
			writer = open(str(i) + '.html', 'w')
			writer.write(driver.page_source)
			writer.close()
if __name__ == '__main__':
	input_file = 'filtered_product_links.txt'
	rfm = RawFilesMaker(input_file)
	rfm.save_htmls()
