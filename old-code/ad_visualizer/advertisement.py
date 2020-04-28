from string import Template

class Advertisement():

	def __init__(self,title='',price=0,description='',image_url=None,image_name=None,product_url=None):

		self.title = title
		self.price = price
		self.image_url = image_url
		self.image_name = image_name
		self.product_url = product_url
		self.description = description

	def set_image(self):
		print("Code to set image")
