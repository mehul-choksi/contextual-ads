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
urls = ['https://www.amazon.in/Poco-Xiaomi-Steel-128GB-Storage/dp/B07GXX2MDQ/ref=asc_df_B07GXX2MDQ/?tag=googleshopdes-21&linkCode=df0&hvadid=397076931806&hvpos=1o2&hvnetw=g&hvrand=6123460887163129379&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062085&hvtargid=pla-521287026379&psc=1&ext_vrnc=hi',
        'https://www.amazon.in/Fashiol-Thermal-Winter-Weather-Assorted/dp/B07ZKGRLWT','https://www.amazon.in/Amazon-Echo-Input/dp/B07C7NSNFM','https://www.amazon.in/Apple-MR972HN-15-4-inch-i7-8850H-Integrated/dp/B07G49GQ56/ref=sr_1_1?adgrpid=59207975216&ext_vrnc=hi&gclid=CjwKCAiApOvwBRBUEiwAcZGdGFOEKOrISp5vcUnbYzZO42Ro8Cun5lWuDBimVy7-y3k-EDmqtlWgSRoCWb0QAvD_BwE&hvadid=294132147740&hvdev=c&hvlocphy=9062085&hvnetw=g&hvpos=1t1&hvqmt=b&hvrand=14163063359626268325&hvtargid=kwd-298999554220&hydadcr=25653_1900983&keywords=macbook+pro+i7+16gb&qid=1578897947&smid=A14CZOWI0VEHLG&sr=8-1','https://www.amazon.in/Adjustable-Xiaomi-Mi-Band-Compatible/dp/B07MTF3FKL','https://www.amazon.in/HP-X1000-Wired-Mouse-Black/dp/B009VCGPSY','https://www.amazon.in/Qube-Fort-Collins-Womens-66118AZ_1_D-red_XL/dp/B07SNZBPSP/ref=asc_df_B07SNZBPSP/?tag=googleshopdes-21&linkCode=df0&hvadid=396984964773&hvpos=1o2&hvnetw=g&hvrand=16742190999110685505&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062085&hvtargid=pla-841970234590&psc=1&ext_vrnc=hi','https://www.amazon.in/Generic-Realistic-Silicone-Vinyl-Lifelike/dp/B01GCQ8AIY','https://www.amazon.in/Generic-Retractable-Recoil-Silver-Black-15018523Mg/dp/B01CZU4UNU/ref=cm_cr_arp_d_product_top?ie=UTF8','https://www.amazon.in/Webby-Princess-Castle-Play-House/dp/B07MHCRYCR/ref=asc_df_B07MHCRYCR/?tag=googleshopdes-21&linkCode=df0&hvadid=397079867672&hvpos=1o2&hvnetw=g&hvrand=10194881061890979571&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062085&hvtargid=pla-862388968074&psc=1&ext_vrnc=hi','https://www.amazon.in/Star-Wars-Force-Awakens-BB-8/dp/B00WHX8Z1O/ref=asc_df_B00WHX8Z1O/?tag=googleshopdes-21&linkCode=df0&hvadid=396989439720&hvpos=1o1&hvnetw=g&hvrand=2226831721202231276&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062085&hvtargid=pla-406246022553&psc=1&ext_vrnc=hi','https://www.amazon.in/Johnsons-Baby-Powder-400g-Free/dp/B06ZY87N76','https://www.amazon.in/Himalaya-7003817-Baby-Powder-700g/dp/B07PSJW32L/ref=asc_df_B07PSJW32L/?tag=googleshopdes-21&linkCode=df0&hvadid=396988722141&hvpos=1o2&hvnetw=g&hvrand=6423595830340887874&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062085&hvtargid=pla-785071390753&psc=1&ext_vrnc=hi','https://www.amazon.in/Mom-World-Baby-Wash-Cleansing/dp/B07MR7TQ8K/ref=asc_df_B07MR7TQ8K/?tag=googleshopdes-21&linkCode=df0&hvadid=396986752551&hvpos=1o4&hvnetw=g&hvrand=13779861699581900869&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062085&hvtargid=pla-890761812167&psc=1&ext_vrnc=hi','https://www.amazon.in/Johnsons-Baby-Cream-100g-Pack/dp/B07FR14YGD','https://www.amazon.in/Mee-Liquid-Laundry-Detergent-Refill/dp/B0789J9K2B']

def getDetails(url):
    f=open('db.txt','a')
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False, headers=headers)
    response = requests.get(url, headers=headers)
    #print(response.text)
    soup = BeautifulSoup(response.content, features="lxml")
    soup2=BeautifulSoup(response.content,"html.parser")

    ###containers1 = soup2.findAll("li", {"class":"s-result-item s-result-card-for-container a-declarative celwidget "})
    #print("containers style 1: ", len(containers1))


    #containers2 = soup2.findAll("li", {"class":"s-result-item s-result-card-for-container s-carded-grid celwidget "})
    #print("containers style 2: ", len(containers2))

    #sponsored_containers = soup2.findAll("li", {"class":"s-result-item celwidget AdHolder"})
    #print("containers style 3 sponsored: ", len(sponsored_containers))

    # most common style
    common_containers = soup2.findAll("li", {"class":"s-result-item celwidget "})
    print("containers style 4 common: ", len(common_containers))

    #special style
    #containers3 = soup2.findAll("li", {"class":"s-result-item s-col-span-12 celwidget "})
    #print("containers style 5 special", len(containers3))###
    title = soup.select("#productTitle")[0].get_text().strip()
    print(title)
    sResultItem =soup.find_all("li", {"class": "s-result-item"})
    dataAsins = [ li['data-asin'] for li in sResultItem ]

    Review_keywords=[]
    categories = []
    if(soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")):
        for li in soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")[0].findAll("li"):
            categories.append(li.get_text().strip())

    price=0
    if(soup.select("#priceblock_saleprice")):
        price = soup.select("#priceblock_saleprice")[0].get_text()

    review_count=0
    if(soup.select("#acrCustomerReviewText")):
        review_count = (soup.select("#acrCustomerReviewText")[0].get_text().split()[0])

    features = []
    for li in soup.select("#feature-bullets ul.a-unordered-list")[0].findAll('li'):
        features.append(li.get_text().strip())

    #print(price)
    #print(categories)
    #print(features)

    jsonObject = {'ASIN':dataAsins,'title': title, 'categories': categories,'price':price ,'features': features , 'review_count': review_count}
    print(json.dumps(jsonObject, indent=2))


for i in urls:
    getDetails(i)
