import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel 

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=str, required=True, help="A username is required"
    )
    
    parser.add_argument(
        'password', type=str, required=True, help="A password is required"
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {"message" : "The username {} is already registered.".format(data['username'])}, 400
        
        user = UserModel(**data) #data['username'], data['password'] keyword:argument
        user.save_to_db()
        
        return {"message" : "User {} registered.".format(data['username'])}, 201
    