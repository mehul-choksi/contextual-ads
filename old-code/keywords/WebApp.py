from flask import Flask,redirect,request,url_for, render_template
from Scraper import Scraper
app = Flask(__name__)

@app.route('/input')
def input():
   #site=request.args.get('website')
   return render_template('Apphtml.html')

@app.route('/scrape')
def scrape():
    site = request.args.get('website',None)
    obj=Scraper()
    keyword_dict = obj.keywords(site)
    # list=[]
    # for key in keyword_dict:
    #     list.append(key + ': ' + str(keyword_dict[key]))
    # keywords =  "".join(list)
    return render_template('Display.html',site=site,keywords=keyword_dict)



if __name__ == '__main__':
   app.run(debug=True,host="0.0.0.0")
