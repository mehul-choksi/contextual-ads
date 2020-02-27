from flask import Flask
from flask import render_template

from advertisement import Advertisement

# This is temporary
import json

app = Flask(__name__)

def fetch_ads():
    """ Fetches advertisements
    """
    ad_arr = []
    with open("corrected.json",'r') as r:
        ads_dict = json.load(r)
        for ad_dict in ads_dict[:3]:
            ad_arr.append(Advertisement(title=ad_dict.get('name'),
            price=500, # har cheeze 500 me
            image_url=ad_dict.get("image_urls")[0],
            image_name = ad_dict.get("image_name"),
            product_url = ad_dict.get("product_url")
            ))
    return ad_arr

@app.route('/display_ads')
def display_ads():
    # read ad from somewhere
    ad_arr = fetch_ads()

    return render_template('./ad_response.html',ads=ad_arr)
