from string import Template

class Advertisement():

	def __init__(self,title='',price=0,description='',image=None):
		
		self.title = title
		self.price = price
		self.image = image
		self.description = description
		self.stringifiedHtml = ''
		
	def set_image(self):

		print("Code to set image")


	def to_html(self):
		s += self.header
		
		s += templated_frame
		
		self.stringifiedHtml = s

	def product_to_div(self):
		frameReader = open('adframe')
		frameContent = frameReader.read()
		frame = Template(frameContent)
		productPrice = ("Get this product for only " + str(self.price))
		d = {"ProductTitle" : self.title, "ProductPrice" : productPrice, "ProductDescription" : self.description}
		templated_frame = frame.substitute(**d)
		self.stringifiedHtml = templated_frame

	def write_as_file(self):
		writer = open('test.html','w')
		writer.write(self.stringifiedHtml)
		writer.close()



def write_as_html(ads):
	readHeader = open('header')
	header = readHeader.read()
	readHeader.close()

	s = header
	for ad in ads:
		s += ad.stringifiedHtml
	
	s += '</div></div>'
	s += '</body>'
	s += '</html>'

	writer = open('ad_response.html', 'w')
	writer.write(s)
	writer.close()
if __name__ == '__main__':

	arr = []

	a1 = Advertisement(title = 'Test advertisement here with heading', price = 42069, description='Preview description for the this product. This text depicts describes the product shortly, so as to inform the user. Upon clicking this, the user will be redirected to the blog post where he can view the full post.')
	a1.product_to_div()
	arr.append(a1)
	
	a2 = Advertisement(title = 'Test 2', price = 982347, description='Description of the second product')
	a2.product_to_div()
	arr.append(a2)

	a3 = Advertisement(title = 'Test 3', price = 1234, description='Description of the third product')
	a3.product_to_div()
	arr.append(a3)

	write_as_html(arr)
	
