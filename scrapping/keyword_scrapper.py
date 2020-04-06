import requests
import json
import requests
from lxml import html
import requests.packages.urllib3.exceptions
from urllib3.exceptions import InsecureRequestWarning
import urllib3
#from lxml import etree
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
cnt=0

def getDetails(json_o):
    url=json_o['product_url']
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False, headers=headers)
    response = requests.get(url, headers=headers)
    #print(response.text)
    soup = BeautifulSoup(response.content, features="lxml")
    soup2=BeautifulSoup(response.content,"html.parser")


    # most common style
    common_containers = soup2.findAll("li", {"class":"s-result-item celwidget "})

    sResultItem =soup.find_all("li", {"class": "s-result-item"})
    dataAsins = [ li['data-asin'] for li in sResultItem ]

    Review_keywords=[]
    categories = []
    if(soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")):
        for li in soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")[0].findAll("li"):
            categories.append(li.get_text().strip())

    review_count=0
    if(soup.select("#acrCustomerReviewText")):
        review_count = (soup.select("#acrCustomerReviewText")[0].get_text().split()[0])

    features = []
    if(soup.select("#feature-bullets ul.a-unordered-list")):
        for li in soup.select("#feature-bullets ul.a-unordered-list")[0].findAll('li'):
            features.append(li.get_text().strip())


    jsonObject = {'title': json_o['name'], 'image_urls':json_o['image_urls'],'image_name':json_o['image_name'],'images':json_o['images'],'product_url':url,'tags':json_o['tags'],'categories': categories ,'features': features , 'review_count': review_count}
    with open('data.json', 'a') as outfile:
        json.dump(jsonObject, outfile)
        outfile.write(',')


input_file = open ('products.json','r',encoding='UTF-8')
json_array = json.load(input_file)
print(len(json_array))

for item in json_array:
    getDetails(item)
    cnt+=1
    print(cnt)
