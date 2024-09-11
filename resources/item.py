import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items.")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # Get store; Check if store exists
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        # Delete item if item exists
        try:
            del items[item_id]
            return {"message": "Item deleted."}, 200
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # Get item if exists
        try:
            item = items[item_id]
        except KeyError:
            abort(404, message="Item not found.")
        else:
            # Update item
            item |= item_data
            return item, 200
        


@blp.route("/item")
class Item(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # Check if item already exist
        for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
                abort(400, "Bad request. Item already exist.")

        # Check if store exists
        if  item_data["store_id"] not in stores:
            abort(404, message="Store not found.")
        
        # Create item UUID
        item_id = uuid.uuid4().hex
        # Create item
        item = {**item_data, "id": item_id}
        # Save item
        items[item_id] = item

        return item, 201