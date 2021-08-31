from flask import Flask, request, Response
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

#Flask
app = Flask(__name__)

#Connection with MongoDB
app.config['MONGO_URI']='mongodb://conteo:admin@cluster0-shard-00-00.qa9gg.mongodb.net:27017,cluster0-shard-00-01.qa9gg.mongodb.net:27017,cluster0-shard-00-02.qa9gg.mongodb.net:27017/PythonServer?ssl=true&replicaSet=atlas-qgslpb-shard-0&authSource=admin&retryWrites=true&w=majority'
mongo = PyMongo(app)

#Settings
CORS(app)

#Routes
@app.route('/', methods=['POST'])
def post():
    product = request.json['product']
    description = request.json['description']
    if product and description:
        id = mongo.db.product.insert(
            {
                'product': product,
                'description': description
            }
        )
        response = {
            'id': str(id),
            'product': product,
            'description': description
        }
        return response
    else:
        return {'message': 'no received'}

@app.route('/', methods=['GET'])
def get():
    products = mongo.db.product.find()
    response = json_util.dumps(products)
    return Response(response, mimetype='application/json')

#Sever
if __name__ == "__main__":
    app.run(port=5000, debug=True)