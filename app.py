from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity as identiy_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import StoreList, Store
from flask import jsonify
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mykey'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login' #changes the authentication endpoint from /auth to /login
jwt = JWT(app, authenticate, identiy_function)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

#@jwt.error_handler
#def customized_error_handler(error):
#    return jsonify({
#        'message': error.description,
#        'code': error.status_code
#    }), error.status_code

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__': #only start the app when app.py is started with python.exe
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)