import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


# Stores
@app.get("/store")
def get_stores():
    return {"Stores": list(stores.values())}


@app.get("/store/<string:store_id>") 
def get_store(store_id):
    # Get store; Check if store exists
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message="Store not found.")


@app.post("/store")
def create_store():
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


@app.delete("/store/<string:store_id>") 
def delete_store(store_id):
    # Delete store if store exists
    try:
        store = stores[store_id]
        del stores[store_id]
        return {"message": "Store deleted."}, 200
    except KeyError:
        abort(404, message="Store not found.")


@app.put("/store/<string:store_id>")
def update_store(store_id):
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




# Items
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>") 
def get_item(item_id):
    # Get store; Check if store exists
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item not found.")


@app.post("/item")
def create_item():
    item_data = request.get_json()

    # Check if 'store_id', 'price', and 'name' key exist in payload.
    if any(key not in item_data for key in ["store_id", "price", "name"]):
        abort(400, "Bad request. Be sure item includes 'store_id', 'price', and 'name' in the JSON payload.")
    
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


@app.delete("/item/<string:item_id>") 
def delete_item(item_id):
    # Delete item if item exists
    try:
        item = items[item_id]
        del items[item_id]
        return {"message": "Item deleted."}, 200
    except KeyError:
        abort(404, message="Item not found.")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()

    # Check if valid keys in payload.
    for key in item_data.keys():
        if key not in ["name", "price"]:
            abort(400, "Bad request. Be sure item only includes 'name', or 'price' in the JSON payload.")

    try:
        # Get item if exists
        item = items[item_id]
    except KeyError:
        abort(404, message="Item not found.")
    else:
        # Update item
        item |= item_data
        return item, 200