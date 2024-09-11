import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


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

    def put(self, store_id):
        store_data = request.get_json()

        # Check if valid keys in payload.
        for key in store_data.keys():
            if key not in ["name"]:
                abort(400, "Bad request. Be sure item only includes 'name' in the JSON payload.")

        try:
            # Get store if exists
            store = stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")
        else:
            # Update store
            store |= store_data
            return store, 200


@blp.route("/store")
class Store(MethodView):
    def get(self):
        return {"Stores": list(stores.values())}
    
    def post(self):
        store_data = request.get_json()
        # Check if 'name' key exist in payload.
        if "name" not in store_data:
            abort(400, "Bad request. Be sure store includes 'name' in the JSON payload.")

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