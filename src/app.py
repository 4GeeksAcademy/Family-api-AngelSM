"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object

initial_members = [

    {
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    },
    {
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    },
    {
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    }
]

for member in initial_members:
    jackson_family.add_member(member)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members', methods=['POST'])
def create_member():
    new_member = request.json
    jackson_family.add_member(new_member)
    if new_member.get('first_name') is None:
        return ('Error! Name is invalid'), 400
    if new_member.get('age') is None or new_member.get('age') <= 0:
        return ('Error! Age is invalid'),400
    if not new_member.get('lucky_numbers'):
        return ('Error! You must have lucky number'),400
    return jsonify(new_member), 201


@app.route('/members/<int:member_id>', methods=['GET'])
def single_member(member_id):
    member = jackson_family.get_member(member_id)
    
    return jsonify({"msg": "Te member showed is:"}, member), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    
    deleted = jackson_family.delete_member(member_id)

    if not deleted :
        return jsonify ({'msg': 'Not found'}), 404
    return jsonify ({'msg': 'Deleted successfully'}),200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
