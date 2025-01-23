import uuid
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import items, stores
from schema import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, "No such item found")

    def delete(self, item_id):

        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, "No such item found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(
        200, ItemSchema
    )  # response decorator must come after arguments if any. Order matters
    def put(
        self, item_data, item_id
    ):  # validaiton data comes before the path variables

        try:

            db_item = items[item_id]

            if "price" in item_data:
                db_item["price"] = item_data["price"]

            if "name" in item_data:
                db_item["name"] = item_data["name"]

            return {"message": "Item updated successfully", "item": db_item}

        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class Item(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return {
            "items": items.values()
        }  # since we specify many=True it will automatically be list so we don't need to convert it to list anymore.

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(
        self, item_data
    ):  # item data is what we get from ItemSchema validation as json. The json data we send goes through our ItemSchema marshmallow and then gets a valid json. Another benefit of marshmallow is it auto generate the parameters for documenting openai

        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, "Item already exists for the store")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return {"item": item}
