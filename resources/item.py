from sqlalchemy.exc import SQLAlchemyError
import uuid
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schema import ItemSchema, ItemUpdateSchema
from models.item import ItemModel
from db import db


blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):

        item = ItemModel.query.get_or_404(item_id)

        try:
            return item
        except KeyError:
            abort(404, "No such item found")

    def delete(self, item_id):

        item = ItemModel.query.get_or_404(item_id)

        db.session.delete(item)
        db.session.commit()

        return {"message": "Item has been deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(
        200, ItemSchema
    )  # response decorator must come after arguments if any. Order matters
    def put(
        self, item_data, item_id
    ):  # validaiton data comes before the path variables

        item = ItemModel.query.get_or_404(item_id)

        if item_data.get("price"):
            item.price = item_data["price"]
        if item_data.get("name"):
            item.name = item_data["name"]
        if item_data.get("store_id"):
            item.store_id = item_data["store_id"]

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class Item(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(
        self, item_data
    ):  # item data is what we get from ItemSchema validation as json. The json data we send goes through our ItemSchema marshmallow and then gets a valid json. Another benefit of marshmallow is it auto generate the parameters for documenting openai

        item = ItemModel(
            **item_data
        )  # basically by **store_data we get all keyword and values from request for the data which are mentioned on ItemModel

        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occured while trying to create a store")

        return item
