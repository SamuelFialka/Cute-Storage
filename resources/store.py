from flask_restful import reqparse, Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': 'Store doent exists'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'The store already exists.'}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()        
            except:
                return {'message': 'Error occured while creating the store.'}, 500
            return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted.'}, 200
        else:
            return {'message': 'Store doesn exists.'}, 404


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.get_items()]}