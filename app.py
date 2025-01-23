import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/stores")
def create_store():
    request_data = request.get_json()

    for store in stores:
        if store["name"] == request_data["name"]:
            abort(400, "Store already exists")
    store_id = uuid.uuid4().hex
    new_store = {**request_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
        or item_data["store_id"] not in stores
    ):
        abort(400, message="price & name & store_id must be send")
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, "Item already exists for the store")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")


@app.get("/stores/<string:store_id>")
def get_store(store_id):

    try:
        return {"store": stores[store_id]}
    except KeyError:
        abort(404, message="Store not found")


@app.get("/items")
def get_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return {"item": items[item_id]}
    except KeyError:
        abort(404, message="Item not found")
