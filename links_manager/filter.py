import hashlib
class Filter():

	def __init__(self, input_file, output_file):
		self.input_file = input_file
		self.output_file = output_file
		self.link_hashes = set()

	def process(self):
		reader = open(self.input_file)
		writer = open('filtered_product_links.txt', 'w')
		for line in reader:
			line = line.strip()
			if self.valid(line):
				try:
					self.link_hashes.add(self.hash_link(line.split('amazon.in/')[1].split('/')[0]))
				except:
					print('unable to hash ')
				writer.write(line + '\n')
				print(line)
			#else:
				#print('invalid')
			
	def valid(self,link):
		#print(link)
		#links with /s/ are meta pages again
		#maybe useful in future
		try:
			if len(link) < 100 or link.find('/s/') !=-1 or link.find('/b/') != -1 or link.find('/s?') != -1 or link.find('/b?') != -1 or link.startswith('javascript') or link.find('gift-cards') != -1:
				#print('eliminated at 1')
				return False
			elif link.find('/help') != -1 or link.find('redirect.html') != -1 or link.find('/customer') != -1 or link.find('search-alias') != -1:
				#print('eliminated at 2')
				return False
			elif link.find('signin') != -1 or link.find('advertising.amazon') != -1 or link.find('#customerReviews') != -1 or link.find('product-reviews') != -1 or link.find('reviewerType') != -1 or link.find('register') != -1 or link.find('mailto') != -1 or link.find('wishlist') != -1:
				#print('eliminated at 3')
				return False
		
			elif self.hash_link(link.split('amazon.in/')[1].split('/')[0]) in self.link_hashes:
				#print('eliminated at 4')
				return False
		except:
			return True
		return True
	def hash_link(self, link):
		result = hashlib.md5(link.encode())
		return result.hexdigest()

if __name__ == '__main__':
	input_file = 'raw_product_links.txt'
	output_file = 'filtered_products_links.txt'

	f = Filter(input_file, output_file)
	f.process()
