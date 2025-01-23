import uuid
from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import stores
from schema import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="No such store")

    def delete(self, store_id):
        try:
            del stores[store_id]
        except KeyError:
            abort(404, message="No such store")


@blp.route("/store")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):

        for store in stores:
            if store["name"] == store_data["name"]:
                abort(400, "Store already exists")
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201
