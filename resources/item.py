from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help = 'This field is required'
                        )
    
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help = 'Every item needs a store id '
                        )
        
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        
        if item:
            print(item)
            return item.json() #to convert the item object into a dictionary
        return {"message":"Item does not exist is db"},404
        
        #return {"item":item}, 200 if item else 404
        
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message" : "The item with name '{}' already exists.".format(name)}, 400
        
        request_data = Item.parser.parse_args()
        
        item = ItemModel(name,**request_data)
        
        try:
            item.save_to_db()
        except:
            return {"message" : "An error occurred while inserting this item."}, 500 #internal server error
        
        return item.json(), 201
        
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            
        return {"message" : "Item {} deleted.".format(name)}
    
    def put(self, name):
        request_data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        
        
        if item is None:    
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data['price']

        item.save_to_db()
        return item.json()
        
class ItemList(Resource):
    def get(self):
        
        return {"items": [item.json() for item in ItemModel.query.all()]}
        #with lambda    
        #return {"items": list(map(lambda x:x.json(), ItemModel.query.all()))}