from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message" : "Store {} not found".format(name)}, 404
        
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message":"The store {} already exists".format(name)}, 400
        
        store = StoreModel(name)
        
        try:
            store.save_to_db()
        except:
            return {"message" : "Something went wrong saving the store {}".format(name)}, 500
        
        return store.json()
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
        
        return {"message" : "Store deleted."}
    
class StoreList(Resource):
    def get(self):
        return {"stores" : [store.json() for store in StoreModel.query.all()]}