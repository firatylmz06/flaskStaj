from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Users"
mongo = PyMongo(app)


@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    username = _json['username']
    lastname = _json['lastname']

    if username and lastname and request.method == 'POST':
        id = mongo.db.userdb.insert_one({'username': username, 'lastname': lastname})
        resp = jsonify("Update Success")
        resp.status_code == 200

        return resp
    else:
        return not_found()


@app.route('/list', methods=['GET'])
def get_user():
    user = mongo.db.userdb.find()
    resp = dumps(user)
    return resp


@app.route('/user/<id>', methods=['GET'])
def find_user(id):
    getuserinfo = mongo.db.userdb.find_one({'_id': ObjectId(id)})
    resp = dumps(getuserinfo)
    return resp


@app.route('/delete/<id>', methods=['POST'])
def delete_user(id):
    mongo.db.userdb.delete_one({'_id': ObjectId(id)})
    resp = jsonify("User Deleted Success")
    resp.status_code = 200
    return resp


@app.route('/update/<id>', methods=['PUT'])
def update_user():
    _json = request.json
    name = _json['name']
    lastname = _json['lastname']

    if name and lastname and request.method == 'PUT':

        mongo.db.userdb.update_one({'name': name, 'lastname': lastname})
        resp = jsonify("Update Success")
        resp.status_code == 200

        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "_main_":
    app.run(debug=True)