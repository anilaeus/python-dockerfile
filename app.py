from flask import Flask, request

app = Flask(__name__)


stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]


@app.get("/stores")
def get_stores():
    return {"stores": stores}


@app.post("/stores")
def create_store():
    request_data = request.get_json()
    print(f"name: {request_data['name']}")
    print(f"items: {request_data['items']}")
    stores.append(request_data)
    return {"stores": stores}, 201


@app.get("/stores/<string:name>")
def get_store(name):
    print(f"Request name is {name} ")
    store = next((store for store in stores if store["name"] == name), None)

    if store is None:
        return {"message": "Store is not found"}, 404

    return {"store": store}


@app.get("/stores/<string:store_name>/items")
def get_store_items(store_name):

    store = next((store for store in stores if store["name"] == store_name), None)

    if store is None:
        return {"message": "No such store exists"}, 404

    return {"store_items": store["items"]}, 200
