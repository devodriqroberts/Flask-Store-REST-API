import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema, StoreUpdateSchema


blp = Blueprint("stores", __name__, description="Operations on stores.")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
    # Get store; Check if store exists
        try:
            return stores[store_id], 200
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        # Delete store if store exists
        try:
            del stores[store_id]
            return {"message": "Store deleted."}, 200
        except KeyError:
            abort(404, message="Store not found.")

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        # Get store if exists
        try:
            store = stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")
        else:
            # Update store
            store |= store_data
            return store, 200


@blp.route("/store")
class Store(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return {"Stores": list(stores.values())}
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # Check if store already exist
        for store in stores:
            if store["name"] == store_data["name"]:
                abort(400, "Bad request. Store already exist.")

        # Create store UUID
        store_id = uuid.uuid4().hex
        # Create store
        store = {"id": store_id, **store_data}
        # Save store
        stores[store_id] = store
        return store, 201