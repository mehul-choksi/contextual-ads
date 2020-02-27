from flask import Flask, request
from flask import render_template

from pymongo import MongoClient
import pprint

from concept_hierarchy import Concept_hierarchy, Node

ch = Concept_hierarchy('test.json')

client = MongoClient("localhost",27017)

db = client.ContextAds
collections = db.Products

app = Flask(__name__)

def query():
    """ Query logic goes here """
    return list(collections.find())

@app.route('/displayProducts')
def display_products():
    result = query()
    return render_template("./index.html",result_list=result)


@app.route('/createNode')
def createNode():
    return render_template('./node_form.html')

@app.route('/create_node', methods=['POST'])
def create_node():
    error_msg = None

    name = request.form.get('name').lower()
    parent = request.form.get('parent').lower()
    synonyms = request.form.get('synonyms').split(',')

    parent_node = ch.lookup.get(parent)
    if parent_node is None:
        error_msg = "Couldn't find parent node"
    else:
        current_node = Node(name)
        current_node.parent = parent
        parent_node.children.append(current_node)

        # TODO:  write updated cf to json file or mongodb

    return render_template('./node_create.html',error_msg=error_msg, **request.form)

@app.route('/createProduct')
def createProduct():
    return render_template('./product_form.html')

@app.route('/create_product', methods=['POST'])
def create_product():
    error_msg = None

    name = request.form.get('name').lower()
    desc = request.form.get('desc').lower()
    tags = request.form.get('tags').split(',')
    price = float(request.form.get('price'))
    link = request.form.get('link')

    record = {
    "name":name,
    "desc":desc,
    "tags":tags,
    "price":price,
    "link":link
    }

    collections.insert(record)

    return render_template('./product_create.html',error_msg=error_msg, **record)

app.run(debug=True)
