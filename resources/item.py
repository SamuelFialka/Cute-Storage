from flask_jwt import jwt_required
from flask_restful import reqparse, Resource
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank.",
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every items needs store id.",
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found.'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'An item with name {} aleready exists'.format(name)}, 400
        
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item was deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'], data['store_id'])
        
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        list(map(lambda item: item.json(), ItemModel.items()))
        return {'items': list(map(lambda x: x.json(), ItemModel.items()))}
