import uuid
from flask import Flask, request
from db import stores, items

app = Flask(__name__)


@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/stores")
def create_store():
    request_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**request_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/stores/<string:store_id>")
def get_store(store_id):

    try:
        return {"store": stores[store_id]}
    except KeyError:
        return {"message": "No such store exists"}, 404


@app.get("/items")
def get_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return {"item": items[item_id]}
    except KeyError:
        return {"message": "No such item has been found"}, 404
