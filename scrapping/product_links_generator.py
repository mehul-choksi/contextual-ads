from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox(executable_path='./geckodriver') # initialize driver


#utility class to scrape product links and append them to links.txt
class LinkScrapper():

	def __init__(self, query_file, output_file,rep=5):
		self.query_file = query_file
		self.output_file = output_file
		self.rep = rep

	def query_to_links(self, query):
		driver.get('http://www.amazon.in')
		links = []
		search_box = driver.find_element_by_xpath("//input[@id='twotabsearchtextbox']")
		search_box.send_keys(query)

		search_button = driver.find_element_by_xpath("//input[@value='Go']")
		search_button.click()


		for i in range(0,self.rep):
			#<a href="/s?k=programming+books&amp;page=2&amp;qid=1576913151&amp;ref=sr_pg_1">Next<span class="a-letter-space"></span><span class="a-letter-space"></span>→</a>
			elements = driver.find_elements_by_xpath("//a[@class='a-link-normal a-text-normal']")

			for element in elements:
				curr_link = element.get_attribute('href')
				links.append(curr_link)

			next_button = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
			next_button.click()

		print(links)
		#links = ['https://www.amazon.in/'+ link for link in links]

		writer = open(self.output_file, 'a')
		for link in links:
			writer.write(link+'\n')
		

	def run(self):
		reader = open(self.query_file)
		for line in reader:
			line = line.strip()
			self.query_to_links(line)

if __name__ == '__main__':
	input_file = 'queries.txt'
	output_file = 'test_links.txt'
	link_scrapper = LinkScrapper(input_file, output_file)
	link_scrapper.run()
	
